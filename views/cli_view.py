"""Couche Vue (V) : Présentation Console / Terminal pour l'architecture MVC.

Cette classe gère exclusivement l'affichage des informations pour l'utilisateur :
- Bannières d'accueil
- Menus des catégories technologiques
- Barre de progression du scraping
- Tableaux formatés des produits extraits et stockés en base
- Résumés statistiques de la base de données SQLite
"""

import sys
from typing import Any, Dict, List

# Assure le support UTF-8 sur les terminaux Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class CLIView:
    """Vue Console MVC : Affichage formaté des données et interactions terminal."""

    # Codes ANSI pour un rendu professionnel dans le terminal
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    RED = "\033[91m"
    GRAY = "\033[90m"

    @classmethod
    def display_banner(cls):
        print(f"\n{cls.CYAN}{cls.BOLD}" + "=" * 78)
        print("   >>> AMAZON TECH SCRAPER & DATABASE PRO  (Architecture MVC) <<<")
        print("   Extraction d'outils technologiques & Persistance en BDD SQL Server (SSMS)")
        print("=" * 78 + f"{cls.RESET}\n")

    @classmethod
    def display_categories_menu(cls, categories: Dict[str, tuple]):
        print(f"{cls.YELLOW}{cls.BOLD}[*] Categories Technologiques Disponibles :{cls.RESET}")
        for key, (label, query) in categories.items():
            print(f"  [{cls.CYAN}{key}{cls.RESET}] {label.ljust(30)} {cls.GRAY}-> '{query}'{cls.RESET}")
        print(f"  [{cls.CYAN}8{cls.RESET}] {cls.BOLD}Recherche personnalisee...{cls.RESET}")
        print(f"  [{cls.CYAN}9{cls.RESET}] {cls.MAGENTA}Consulter les produits deja enregistres en BDD{cls.RESET}")
        print(f"  [{cls.CYAN}0{cls.RESET}] {cls.RED}Quitter{cls.RESET}\n")

    @classmethod
    def display_progress(cls, message: str, percentage: int):
        bar_length = 30
        filled = int(bar_length * percentage // 100)
        bar = "#" * filled + "-" * (bar_length - filled)
        msg_clean = message[:45].ljust(45)
        print(f"\r  [{cls.GREEN}{bar}{cls.RESET}] {percentage}% | {msg_clean}", end="", flush=True)
        if percentage >= 100:
            print()

    @classmethod
    def display_log(cls, message: str):
        print(f"  {cls.GRAY}[INFO]{cls.RESET} {message}")

    @classmethod
    def display_success(cls, message: str):
        print(f"\n{cls.GREEN}{cls.BOLD}[SUCCES] {message}{cls.RESET}")

    @classmethod
    def display_error(cls, message: str):
        print(f"\n{cls.RED}{cls.BOLD}[ERREUR] {message}{cls.RESET}")

    @classmethod
    def display_products_table(cls, products: List[Dict[str, Any]], title: str = "PRODUITS TECH EN BASE"):
        if not products:
            print(f"\n{cls.YELLOW}Aucun produit a afficher.{cls.RESET}\n")
            return

        print(f"\n{cls.BOLD}{cls.CYAN}[LISTE] {title} ({len(products)} articles) :{cls.RESET}")
        print("-" * 105)
        # En-têtes du tableau
        header = (
            f"{'#':<3} | {'ASIN':<10} | {'PRIX':<10} | {'NOTE':<6} | {'AVIS':<8} | {'TITRE TECH':<55}"
        )
        print(f"{cls.BOLD}{header}{cls.RESET}")
        print("-" * 105)

        for idx, p in enumerate(products, 1):
            asin = str(p.get("asin") or "-")[:10]
            if p.get("price_val") is not None:
                curr = p.get("currency") or ""
                price = f"{p.get('price_val')} {curr}".strip()[:10]
            else:
                price = str(p.get("price_raw") or "-")[:10]
            rating = f"{p.get('rating_score')}/5" if p.get("rating_score") else "-"
            reviews = str(p.get("reviews_count") or "-")[:8]
            prod_title = str(p.get("title") or "")
            if len(prod_title) > 52:
                prod_title = prod_title[:49] + "..."

            print(
                f"{idx:<3} | {cls.YELLOW}{asin:<10}{cls.RESET} | {cls.GREEN}{price:<10}{cls.RESET} | "
                f"{rating:<6} | {reviews:<8} | {prod_title:<55}"
            )

        print("-" * 105 + "\n")

    @classmethod
    def display_db_summary(cls, stats: Dict[str, Any]):
        print(f"\n{cls.MAGENTA}{cls.BOLD}[STATS] Statistiques Globales de la Base de Donnees SQL Server :{cls.RESET}")
        print(f"  * Total Produits Tech stockes : {cls.BOLD}{stats.get('total_products', 0)}{cls.RESET}")
        print(f"  * Total Sessions de scraping  : {cls.BOLD}{stats.get('total_sessions', 0)}{cls.RESET}")
        print(f"  * Prix moyen des articles     : {cls.GREEN}{stats.get('avg_price', 0)} EUR/USD {cls.RESET}")
        print(f"  * Note moyenne des clients    : {stats.get('avg_rating', 0)} / 5")
        print(f"  * Produits eligibles Prime    : {stats.get('total_prime', 0)}\n")

    @classmethod
    def display_sessions_history(cls, sessions: List[Dict[str, Any]]):
        if not sessions:
            print(f"\n{cls.YELLOW}Aucune session enregistree pour le moment.{cls.RESET}\n")
            return

        print(f"\n{cls.CYAN}{cls.BOLD}[HISTORIQUE] Sessions de scraping en BDD :{cls.RESET}")
        print("-" * 85)
        print(f"{'ID':<4} | {'DATE':<19} | {'STATUT':<10} | {'ARTICLES':<8} | {'RECHERCHE'}")
        print("-" * 85)
        for s in sessions:
            status_color = cls.GREEN if s['status'] == 'completed' else (cls.RED if s['status'] == 'error' else cls.YELLOW)
            print(
                f"#{s['id']:<3} | {str(s.get('started_at'))[:19]:<19} | "
                f"{status_color}{s.get('status', ''):<10}{cls.RESET} | "
                f"{s.get('products_count', 0):<8} | {s.get('query', '')}"
            )
        print("-" * 85 + "\n")
