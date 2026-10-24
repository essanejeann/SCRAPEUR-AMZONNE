"""Module de Scraping Amazon Haute Performance utilisant Selenium (undetected-chromedriver)
et parsing instantané DOM avec BeautifulSoup4.

Fonctionnalités :
- Bipasse anti-bot Amazon (sans écran d'erreur ni blocage CDC).
- Maintien d'identité / session persistante via profil Chrome utilisateur (cookies, localisation).
- Extraction résiliente avec fallbacks multi-niveaux (Titre, Prix, ASIN, URL, Note, Avis, Image, Badges).
- Progression en direct via callbacks.
- Export direct CSV et JSON.
"""

import csv
import json
import logging
import os
import re
import time
import urllib.parse
from datetime import datetime, timezone
from typing import Callable, Dict, List, Optional

from bs4 import BeautifulSoup
import undetected_chromedriver as uc

logger = logging.getLogger("amazon_scraper")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Monkeypatch sécurisé pour la destruction du driver sous Windows
def _safe_chrome_del(self):
    try:
        self.quit()
    except Exception:
        pass

try:
    uc.Chrome.__del__ = _safe_chrome_del
except Exception:
    pass


class AmazonScraper:
    DEFAULT_DOMAIN = "amazon.com"
    AVAILABLE_DOMAINS = {
        "amazon.fr": "Amazon France (amazon.fr)",
        "amazon.com": "Amazon USA (amazon.com)",
        "amazon.de": "Amazon Allemagne (amazon.de)",
        "amazon.co.uk": "Amazon UK (amazon.co.uk)",
        "amazon.es": "Amazon Espagne (amazon.es)",
        "amazon.it": "Amazon Italie (amazon.it)",
        "amazon.ca": "Amazon Canada (amazon.ca)",
    }

    SORT_OPTIONS = {
        "relevance": "",
        "price_asc": "&s=price-asc-rank",
        "price_desc": "&s=price-desc-rank",
        "review_rank": "&s=review-rank",
        "date_desc": "&s=date-desc-rank",
    }

    def __init__(
        self,
        domain: str = "amazon.com",
        user_data_dir: Optional[str] = None,
        headless: bool = False,
    ):
        self.domain = domain if domain in self.AVAILABLE_DOMAINS else self.DEFAULT_DOMAIN
        self.user_data_dir = os.path.abspath(user_data_dir) if user_data_dir else None
        self.headless = headless
        self.driver: Optional[uc.Chrome] = None

    def _init_driver(self) -> uc.Chrome:
        """Initialise une instance furtive de Google Chrome."""
        options = uc.ChromeOptions()
        if self.headless:
            options.add_argument("--headless=new")
        
        options.add_argument("--window-size=1440,900")
        
        if self.user_data_dir:
            os.makedirs(self.user_data_dir, exist_ok=True)
            options.add_argument(f"--user-data-dir={self.user_data_dir}")

        driver = uc.Chrome(options=options)
        return driver

    def close(self):
        """Ferme proprement le navigateur."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            finally:
                self.driver = None

    def _clean_product_url(self, href: str, asin: str) -> str:
        """Construit une URL Amazon propre et directe sans tracking superflu."""
        base = f"https://www.{self.domain}"
        if asin:
            return f"{base}/dp/{asin}"
        if not href:
            return ""
        if href.startswith("/"):
            href = f"{base}{href}"
        # Nettoyage des paramètres d'affiliation/recherche
        clean_url = href.split("?")[0].split("/ref=")[0]
        return clean_url or href

    def _parse_card(self, card) -> Optional[Dict]:
        """Extrait l'ensemble des données d'une carte produit avec fallbacks robustes."""
        asin = card.get("data-asin", "").strip()
        
        # 1. Titre complet (Marque + Modèle détaillé)
        candidates = []
        for sel in [
            "div[data-cy='title-recipe']",
            "h2 a span",
            "h2 span",
            "h2",
            "a.a-link-normal[href*='/dp/'] span",
            ".a-size-medium",
            ".a-size-base-plus",
        ]:
            el = card.select_one(sel)
            if el:
                txt = re.sub(r"\s+", " ", el.get_text(" ", strip=True))
                if txt and len(txt) > 3:
                    candidates.append(txt)
        title = max(candidates, key=len) if candidates else ""

        if not title:
            return None

        # 2. Lien produit
        link_el = card.select_one(
            "h2 a, a.a-link-normal[href*='/dp/'], a[data-cy='title-recipe'], a.a-text-normal, a.a-link-normal"
        )
        raw_href = link_el.get("href", "") if link_el else ""
        product_url = self._clean_product_url(raw_href, asin)

        # 3. Prix
        price_el = card.select_one(".a-price .a-offscreen, .a-price-whole, span[data-a-color='base'] .a-offscreen")
        price_raw = price_el.get_text(strip=True) if price_el else ""
        
        # Valeur numérique estimée du prix
        price_val = None
        currency = ""
        if price_raw:
            # Devise (ex: $, €, £, XOF, etc.)
            curr_match = re.search(r"([^\d\s,.]+)", price_raw)
            if curr_match:
                currency = curr_match.group(1).strip()

            num_str = re.sub(r"[^\d,.]", "", price_raw.replace("\xa0", " "))
            if num_str:
                # Si format 17,547 ou 1,299.99
                if "," in num_str and "." in num_str:
                    # ex: 1,299.99 ou 1.299,99
                    if num_str.rfind(".") > num_str.rfind(","):
                        # 1,299.99
                        cleaned_num = num_str.replace(",", "")
                    else:
                        # 1.299,99
                        cleaned_num = num_str.replace(".", "").replace(",", ".")
                elif "," in num_str:
                    parts = num_str.split(",")
                    # Si après la virgule on a exactement 3 chiffres (ex: 20,948), c'est un millier
                    if len(parts) == 2 and len(parts[1]) == 3 and currency in ["XOF", "JPY", "KRW", "USD", "EUR"]:
                        cleaned_num = num_str.replace(",", "")
                    elif len(parts) == 2 and len(parts[1]) == 2:
                        cleaned_num = num_str.replace(",", ".")
                    else:
                        cleaned_num = num_str.replace(",", "")
                else:
                    cleaned_num = num_str

                try:
                    price_val = float(cleaned_num)
                except ValueError:
                    price_val = None

        # 4. Note (Rating)
        rating_el = card.select_one(
            "i[class*='a-star-'] .a-icon-alt, span.a-icon-alt, [aria-label*='stars'], [aria-label*='étoiles']"
        )
        rating_raw = rating_el.get_text(strip=True) if rating_el else ""
        rating_score = None
        if rating_raw:
            score_match = re.search(r"(\d+[\.,]\d+|\d+)", rating_raw)
            if score_match:
                try:
                    rating_score = float(score_match.group(1).replace(",", "."))
                except ValueError:
                    rating_score = None

        # 5. Nombre d'avis (Reviews)
        reviews_candidates = card.select(
            "a[href*='customerReviews'] span, span[aria-label*='ratings'], span[aria-label*='évaluations'], a[href*='reviews'] span, span.a-size-base.s-underline-text"
        )
        reviews_raw = ""
        for rc in reviews_candidates:
            txt = rc.get_text(strip=True)
            if "feedback" in txt.lower() or "avis sur l'annonce" in txt.lower():
                continue
            if re.search(r"\d", txt):
                reviews_raw = txt
                break

        reviews_count = None
        if reviews_raw:
            clean_rev = reviews_raw.replace("(", "").replace(")", "").strip()
            k_match = re.search(r"(\d+[\.,]?\d*)\s*[kK]", clean_rev)
            if k_match:
                try:
                    reviews_count = int(float(k_match.group(1).replace(",", ".")) * 1000)
                except ValueError:
                    reviews_count = None
            else:
                digits = re.sub(r"[^\d]", "", clean_rev)
                if digits:
                    reviews_count = int(digits)

        # 6. Image
        img_el = card.select_one("img.s-image")
        image_url = ""
        if img_el:
            image_url = img_el.get("src") or img_el.get("data-image-load") or ""
            # Si possible, prendre la version haute résolution dans srcset
            srcset = img_el.get("srcset", "")
            if srcset:
                parts = srcset.split(",")
                if parts:
                    last_part = parts[-1].strip().split(" ")[0]
                    if last_part.startswith("http"):
                        image_url = last_part

        # 7. Badges (Prime, Sponsorisé, Best Seller)
        is_sponsored = bool(
            card.select_one("span.puis-sponsored-label-text, [data-component-type='sp-sponsored-result']")
            or "sponsorisé" in card.get_text().lower()
            or "sponsored" in card.get_text().lower()
        )
        is_prime = bool(card.select_one("i.a-icon-prime"))
        badge_el = card.select_one("span.a-badge-label, span.a-badge-text")
        badge = badge_el.get_text(strip=True) if badge_el else ""

        return {
            "asin": asin,
            "title": title,
            "price_raw": price_raw,
            "price_val": price_val,
            "currency": currency,
            "rating_score": rating_score,
            "rating_raw": rating_raw,
            "reviews_count": reviews_count,
            "reviews_raw": reviews_raw,
            "product_url": product_url,
            "image_url": image_url,
            "is_sponsored": is_sponsored,
            "is_prime": is_prime,
            "badge": badge,
            "domain": self.domain,
            "scraped_at_utc": datetime.now(timezone.utc).isoformat(),
        }

    def scrape(
        self,
        query: str,
        max_products: int = 30,
        sort_by: str = "relevance",
        callback: Optional[Callable[[str, int], None]] = None,
    ) -> List[Dict]:
        """Exécute la recherche et extrait les produits sur une ou plusieurs pages."""
        if not query or not query.strip():
            raise ValueError("Le terme de recherche ne peut pas être vide.")

        query = query.strip()
        sort_suffix = self.SORT_OPTIONS.get(sort_by, "")
        products: List[Dict] = []
        seen_asins = set()

        def notify(msg: str, progress: int):
            logger.info(f"[{progress}%] {msg}")
            if callback:
                try:
                    callback(msg, progress)
                except Exception:
                    pass

        try:
            notify("Initialisation du navigateur furtif Selenium...", 5)
            self.driver = self._init_driver()

            # Warm-up de la session humaine sur la page d'accueil
            notify(f"Connexion et préparation de session sur {self.domain}...", 10)
            self.driver.get(f"https://www.{self.domain}")
            time.sleep(2.5)

            page = 1
            max_pages = 5  # Limite de sécurité

            while len(products) < max_products and page <= max_pages:
                page_param = f"&page={page}" if page > 1 else ""
                url = f"https://www.{self.domain}/s?k={urllib.parse.quote_plus(query)}{page_param}{sort_suffix}"
                
                notify(f"Chargement de la page {page} ({self.domain})...", min(15 + (page - 1) * 20, 80))
                self.driver.get(url)
                
                # Attente dynamique et défilement doux pour charger les images en lazy-load
                time.sleep(3.0)

                # Gestion d'un éventuel challenge temporaire
                title_lower = (self.driver.title or "").lower()
                if "sorry! something went wrong" in title_lower or "toutes nos excuses" in title_lower:
                    logger.warning("Écran temporaire détecté, tentative de rafraîchissement...")
                    time.sleep(2)
                    self.driver.refresh()
                    time.sleep(3)
                    title_lower = (self.driver.title or "").lower()
                    if "sorry! something went wrong" in title_lower or "toutes nos excuses" in title_lower:
                        raise RuntimeError("Amazon a bloqué la requête (Erreur 503 / Anti-bot).")

                if "saisissez les caractères" in title_lower or "type the characters" in title_lower:
                    raise RuntimeError("Amazon demande un CAPTCHA manuel.")

                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
                time.sleep(1.0)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1.0)

                # Analyse de la page
                page_source = self.driver.page_source
                soup = BeautifulSoup(page_source, "html.parser")

                cards = soup.select('div[data-component-type="s-search-result"]')
                if not cards:
                    # Fallback sur les divs avec data-asin valide
                    cards = [c for c in soup.select("div[data-asin]") if c.get("data-asin")]

                if not cards:
                    # Si aucun résultat et pas d'erreur explicite
                    notify(f"Fin des résultats ou aucun article trouvé sur la page {page}.", 90)
                    break

                page_new_count = 0
                for card in cards:
                    if len(products) >= max_products:
                        break
                    
                    parsed = self._parse_card(card)
                    if parsed:
                        asin = parsed["asin"]
                        if asin and asin in seen_asins:
                            continue
                        if asin:
                            seen_asins.add(asin)
                        
                        products.append(parsed)
                        page_new_count += 1

                notify(
                    f"Page {page} analysée : +{page_new_count} articles extraits (Total: {len(products)}/{max_products})",
                    min(20 + int((len(products) / max_products) * 75), 95),
                )

                if page_new_count == 0:
                    break

                page += 1

            notify(f"Scraping terminé avec succès : {len(products)} articles récupérés.", 100)
            return products

        finally:
            self.close()

    @staticmethod
    def export_csv(products: List[Dict], filepath: str) -> str:
        """Exporte les résultats au format CSV encodé UTF-8-BOM."""
        if not products:
            return filepath
        fieldnames = list(products[0].keys())
        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(products)
        return filepath

    @staticmethod
    def export_json(products: List[Dict], filepath: str) -> str:
        """Exporte les résultats au format JSON propre."""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        return filepath
