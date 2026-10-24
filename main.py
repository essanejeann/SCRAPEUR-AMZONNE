"""Point d'entrée principal de l'application Amazon Tech Scraper (Architecture MVC).

Exécution :
    - Mode interactif :
        python main.py
    - Mode ligne de commande directe :
        python main.py --query "laptop rtx 4070" --max 20 --headless
    - Consultation de la base de données :
        python main.py --show-db
"""

import sys
import argparse

import config
from controllers import ScraperController
from views import CLIView


def interactive_menu(controller: ScraperController):
    """Boucle interactive en console pour sélectionner et lancer le scraping."""
    while True:
        CLIView.display_banner()
        CLIView.display_categories_menu(config.TECH_CATEGORIES)

        try:
            choice = input("> Choisissez une option [0-9] : ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nArrêt.")
            break

        if choice == "0":
            print("\nAu revoir !")
            break

        elif choice == "9":
            controller.show_database_contents()
            input("\nAppuyez sur Entrée pour revenir au menu...")

        elif choice in config.TECH_CATEGORIES:
            label, default_query = config.TECH_CATEGORIES[choice]
            print(f"\nVous avez sélectionné : {CLIView.BOLD}{label}{CLIView.RESET}")
            
            custom_q = input(f"Mot-clé de recherche (Entrée pour '{default_query}') : ").strip()
            query = custom_q if custom_q else default_query

            max_p_input = input("Nombre maximum d'articles (défaut: 15) : ").strip()
            max_products = int(max_p_input) if max_p_input.isdigit() else 15

            domain = input("Domaine Amazon (défaut: amazon.com, ou amazon.fr) : ").strip()
            domain = domain if domain else "amazon.com"

            controller.run_scraping(
                query=query,
                category=label,
                domain=domain,
                max_products=max_products,
                headless=False,
            )
            input("\nAppuyez sur Entrée pour revenir au menu...")

        elif choice == "8":
            query = input("\nEntrez votre recherche personnalisée (ex: 'souris gamer sans fil') : ").strip()
            if not query:
                print("Recherche vide annulée.")
                continue

            max_p_input = input("Nombre maximum d'articles (défaut: 15) : ").strip()
            max_products = int(max_p_input) if max_p_input.isdigit() else 15

            domain = input("Domaine Amazon (défaut: amazon.com, ou amazon.fr) : ").strip()
            domain = domain if domain else "amazon.com"

            controller.run_scraping(
                query=query,
                category="Personnalisé",
                domain=domain,
                max_products=max_products,
                headless=False,
            )
            input("\nAppuyez sur Entrée pour revenir au menu...")

        else:
            print("\nOption non reconnue, veuillez réessayer.")


def main():
    parser = argparse.ArgumentParser(
        description="Amazon Tech Scraper - Stockage en BDD SQLite (Architecture MVC)"
    )
    parser.add_argument("--query", "-q", type=str, help="Terme de recherche tech à scraper")
    parser.add_argument("--category", "-c", type=str, default="Tech", help="Nom de la catégorie")
    parser.add_argument("--domain", "-d", type=str, default="amazon.com", help="Domaine Amazon (ex: amazon.com, amazon.fr)")
    parser.add_argument("--max", "-m", type=int, default=15, help="Nombre max d'articles (défaut: 15)")
    parser.add_argument("--sort", "-s", type=str, default="relevance", help="Tri (relevance, price_asc, price_desc, review_rank)")
    parser.add_argument("--headless", action="store_true", help="Lancer Chrome en arrière-plan sans fenêtre")
    parser.add_argument("--show-db", action="store_true", help="Afficher les données déjà présentes en BDD et quitter")

    args = parser.parse_args()
    controller = ScraperController()

    if args.show_db:
        CLIView.display_banner()
        controller.show_database_contents()
        sys.exit(0)

    if args.query:
        CLIView.display_banner()
        controller.run_scraping(
            query=args.query,
            category=args.category,
            domain=args.domain,
            max_products=args.max,
            sort_by=args.sort,
            headless=args.headless,
        )
    else:
        interactive_menu(controller)


if __name__ == "__main__":
    main()
