"""Couche Contrôleur (C) : Orchestrateur de l'application Amazon Tech Scraper.

Fait le lien entre :
- Le Modèle (persistance BDD SQLite via ProductRepository)
- La Vue (affichage console via CLIView)
- Le Moteur de scraping (AmazonScraper)
"""

import os
import logging
from typing import Optional, List, Dict, Any

from models import init_db, ProductRepository
from views import CLIView
from scrapers.amazon_scraper import AmazonScraper
import config

logger = logging.getLogger("scraper_controller")


class ScraperController:
    """Contrôleur principal de l'architecture MVC."""

    def __init__(self):
        # Initialisation de la base de données SQLite
        init_db()

    def run_scraping(
        self,
        query: str,
        category: str = "Tech",
        domain: str = "amazon.com",
        max_products: int = 15,
        sort_by: str = "relevance",
        headless: bool = False,
        export_files: bool = False,
    ) -> List[Dict[str, Any]]:
        """Orchestre la mission de scraping et l'enregistrement en base."""
        CLIView.display_log(f"Initialisation de la session BDD pour '{query}'...")

        # 1. Enregistrement de la session dans le Modèle (BDD)
        session_id = ProductRepository.create_session(
            query=query,
            domain=domain,
            category=category,
            max_products=max_products,
            sort_by=sort_by,
        )
        CLIView.display_log(f"Session #{session_id} créée en base SQL Server.")

        # 2. Callback de progression pour la Vue
        def on_progress(msg: str, pct: int):
            CLIView.display_progress(msg, pct)

        # 3. Exécution du scraping
        scraper = None
        try:
            scraper = AmazonScraper(
                domain=domain,
                user_data_dir=config.CHROME_PROFILE_DIR,
                headless=headless,
            )

            products = scraper.scrape(
                query=query,
                max_products=max_products,
                sort_by=sort_by,
                callback=on_progress,
            )

            # 4. Enregistrement des résultats en base de données (Modèle)
            ProductRepository.complete_session(
                session_id=session_id,
                products_data=products,
                category=category,
                domain=domain,
            )

            # 5. Export de sauvegarde fichiers si activé
            if export_files and products:
                AmazonScraper.export_csv(products, config.RESULTS_FILE_CSV)
                AmazonScraper.export_json(products, config.RESULTS_FILE_JSON)

            # 6. Notification de succès et affichage via la Vue
            CLIView.display_success(
                f"{len(products)} articles tech ont été enregistrés avec succès dans la base de données SQL Server !"
            )

            # Affichage du tableau formaté
            CLIView.display_products_table(products, title=f"RÉSULTATS DE LA SESSION #{session_id} : {query}")

            # Affichage des statistiques de la base
            stats = ProductRepository.get_database_stats()
            CLIView.display_db_summary(stats)

            return products

        except Exception as e:
            logger.exception("Erreur lors de l'exécution du contrôleur")
            ProductRepository.fail_session(session_id, str(e))
            CLIView.display_error(str(e))
            return []

        finally:
            if scraper:
                try:
                    scraper.close()
                except Exception:
                    pass

    def show_database_contents(self, search: Optional[str] = None, limit: int = 30):
        """Affiche les produits et l'historique déjà stockés en BDD."""
        CLIView.display_log("Lecture des données dans la base SQL Server...")
        products = ProductRepository.list_products(search=search, limit=limit)
        sessions = ProductRepository.list_sessions(limit=10)
        stats = ProductRepository.get_database_stats()

        CLIView.display_db_summary(stats)
        CLIView.display_sessions_history(sessions)
        CLIView.display_products_table(products, title="DERNIERS PRODUITS ENREGISTRÉS EN BASE")
