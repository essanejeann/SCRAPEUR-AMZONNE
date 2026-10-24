"""Configuration centralisée pour Amazon Tech Scraper.

Prend en charge :
- Microsoft SQL Server (utilisable directement dans SQL Server Management Studio - SSMS)
- SQLite (local de secours)
"""

import os
import tempfile

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# ── Choix du SGBD : "mssql" (SQL Server / SSMS) ou "sqlite" ──────────────────
DB_ENGINE_TYPE = "mssql"

# Configuration Microsoft SQL Server (pour SQL Server Management Studio)
MSSQL_SERVER = "localhost"
MSSQL_DATABASE = "AmazonTechDB"
MSSQL_DRIVER = "ODBC Driver 18 for SQL Server"
MSSQL_URI = (
    f"mssql+pyodbc://{MSSQL_SERVER}/{MSSQL_DATABASE}?"
    f"driver={MSSQL_DRIVER.replace(' ', '+')}&"
    "trusted_connection=yes&TrustServerCertificate=yes"
)

# Configuration SQLite (secours)
SQLITE_PATH = os.path.join(BASE_DIR, "tech_products.db")
SQLITE_URI = f"sqlite:///{SQLITE_PATH}"

DATABASE_URI = MSSQL_URI if DB_ENGINE_TYPE == "mssql" else SQLITE_URI

# Profil Chrome isolé dans le dossier temporaire du système
CHROME_PROFILE_DIR = os.path.join(tempfile.gettempdir(), "amazon_scraper_profile")

# Catégories technologiques prédéfinies pour Amazon
TECH_CATEGORIES = {
    "1": ("Laptops & PC Portables", "laptop ordinateur portable"),
    "2": ("Cartes Graphiques (GPU)", "carte graphique RTX"),
    "3": ("Smartphones & Tablettes", "smartphone android iphone"),
    "4": ("Casques & Audio Connecté", "casque bluetooth sans fil"),
    "5": ("SSD NVMe & Stockage", "ssd nvme externe"),
    "6": ("Écrans & Moniteurs Tech", "ecran pc gaming 144hz"),
    "7": ("Accessoires & Outils Tech", "hub usb c multiport connectique"),
}
