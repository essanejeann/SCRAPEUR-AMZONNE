# Amazon Tech Scraper — Architecture MVC & SQL Server (SSMS)

Application de scraping et d'analyse d'outils et matériels technologiques sur Amazon (**sans interface web**, 100% autonome en ligne de commande), avec persistance relationnelle directe dans **Microsoft SQL Server (SQL Server Management Studio - SSMS)** et respect strict du patron de conception **Modèle-Vue-Contrôleur (MVC)**.

---

## Aperçu Direct des Données pour le Professeur (Sur GitHub)

Le professeur peut visualiser l'intégralité du projet et des données directement dans son navigateur :

1. **Le script SQL complet de la base** : [`database_dump.sql`](database_dump.sql) *(création de la base, des tables et insertion des 15 articles technologiques)*.
2. **Tableau des 15 articles technologiques extraits et enregistrés dans SQL Server** :

| # | ASIN | Prix | Note | Avis | Modèle & Caractéristiques Techniques |
| :-: | :---: | :---: | :---: | :---: | :--- |
| **1** | `B0DY2T14P6` | 289.00 € | ★ 4.2 / 5 | 175 | **HP 15-fd0001sf Ordinateur Portable 15,6" FHD** |
| **2** | `B0HG52H23H` | 219.99 € | ★ 4.6 / 5 | 5 | **Ordinateur Portable Win 11 Laptop, 15,6" PC Portable** |
| **3** | `B0GQJ8TY68` | 249.99 € | ★ 4.0 / 5 | 97 | **ASUS CM1505CM4A-S70121 15.6 Pouces FHD (1920 x 1080)** |
| **4** | `B0HKHVKM2S` | 299.99 € | ★ 5.0 / 5 | 12 | **Ordinateur Portable 15,6 Pouces IPS FHD, Core i3** |
| **5** | `B0B8QYXY9H` | 419.00 € | ★ 4.2 / 5 | 59 | **Acer Aspire Go 17 \| PC Portable \| 17.3" \| Intel** |
| **6** | `B0CPJNNLR4` | 549.00 € | ★ 4.3 / 5 | 126 | **Lenovo FullHD 15,6 Ordinateur Portable Gaming** |
| **7** | `B0H11DFC26` | 249.99 € | ★ 4.4 / 5 | 63 | **Ordinateur Portable 14 Pouces N4020 SSD** |
| **8** | `B0HFZ78WPC` | 369.99 € | ★ 5.0 / 5 | 1 | **Ordinateur Portable 16" Core i3-1000NG4** |
| **9** | `B0FXRFG5B8` | 279.99 € | ★ 4.1 / 5 | 51 | **Ordinateur Portable 14 Pouces Celeron N5095** |
| **10** | `B0GX64X14Q` | 299.99 € | ★ 5.0 / 5 | 1 | **Lenovo Chrome \| Laptop \| Kompanio 540 \| 8Go** |
| **11** | `B0H6M57QGJ` | - | ★ 4.0 / 5 | 15 | **PINSTONE PC Portable de 14 Pouces Celeron N4000** |
| **12** | `B0BBKYTKXR` | 359.00 € | ★ 4.3 / 5 | 24 | **Acer Chromebook Plus 514 \| 14" WUXGA \| Core 3** |
| **13** | `B0H3F32J2S` | 218.49 € | ★ 3.0 / 5 | 23 | **Ordinateur Portable 15,6 Pouces 8 Go RAM, SSD 256** |
| **14** | `B0HFWTZ59X` | 499.99 € | ★ 4.0 / 5 | 1 | **Lenovo IdeaPad Slim 3 \| Laptop \| R3 \| 8Go \| 512GB** |
| **15** | `B0FXRDG7P5` | 279.99 € | ★ 4.1 / 5 | 51 | **Ordinateur Portable 14 Pouces Celeron N5095** |

---

## Comment Voir les Données dans SQL Server Management Studio (SSMS)

Toutes les données extraites sont directement enregistrées dans votre instance locale **Microsoft SQL Server** dans la base de données **`AmazonTechDB`**.

### 1. Ouvrir SSMS
1. Lancez **SQL Server Management Studio**.
2. Dans la fenêtre de connexion :
   - **Type de serveur** : Moteur de base de données (Database Engine)
   - **Nom du serveur** : `localhost` (ou `.`)
   - **Authentification** : Authentification Windows
3. Cliquez sur **Se connecter** (Connect).

### 2. Accéder aux Tables
Dans l'**Explorateur d'objets** (volet de gauche) :
1. Développez **Bases de données** (Databases) → vous verrez **`AmazonTechDB`**.
2. Développez **Tables** → vous trouverez :
   - **`dbo.products`** : Contient tous les articles tech scrapés (titre, ASIN, prix, note, avis, etc.).
   - **`dbo.scraping_sessions`** : Contient chaque mission de scraping (date, recherche, statut).

### 3. Exécuter des Requêtes SQL dans SSMS
Cliquez sur **Nouvelle requête** (New Query) en haut à gauche et exécutez (`F5`) :

```sql
USE AmazonTechDB;
GO

-- 1. Voir tous les articles technologiques enregistrés
SELECT id, asin, title, price_raw, rating_score, reviews_count, product_url 
FROM products;

-- 2. Voir les produits les mieux notés
SELECT title, price_raw, rating_score 
FROM products 
ORDER BY rating_score DESC;

-- 3. Voir l'historique des sessions de scraping
SELECT id, query_text, started_at, status, products_count 
FROM scraping_sessions;
```

---

## Comment Activer et Lancer le Scrapeur

Suivez ces 3 étapes simples pour activer et utiliser le scrapeur :

### Étape 1 : Ouvrir PowerShell dans le dossier du projet
```powershell
cd "c:\Users\PC\Desktop\repertoi iit\SCRAPEUR AMAZONE"
```

### Étape 2 : Activer l'environnement virtuel Python
```powershell
.\.venv\Scripts\Activate.ps1
```
*(Si une politique d'exécution bloque le script, lancez directement : `.\.venv\Scripts\python.exe main.py`)*

### Étape 3 : Vérifier les dépendances
```powershell
pip install -r requirements.txt
```

---

## Méthodes de Lancement du Scrapeur

### Méthode 1 : Mode Interactif (Recommandé)
Lance un menu guidé dans votre terminal :
```powershell
python main.py
```
Ce menu vous permet de :
- Choisir directement une catégorie technologique prédéfinie (*Laptops, Cartes Graphiques, Smartphones, Casques, SSD, Écrans*).
- Taper une recherche libre personnalisée.
- Définir le nombre d'articles à récupérer.
- Choisir le domaine Amazon (`amazon.com`, `amazon.fr`, etc.).

### Méthode 2 : Lancement Direct en Ligne de Commande
Pour scraper directement un produit tech sans passer par le menu :
```powershell
# Exemple 1 : Récupérer 15 ordinateurs portables
python main.py --query "laptop dell" --max 15

# Exemple 2 : Récupérer 10 cartes graphiques sur Amazon France
python main.py --query "carte graphique RTX 4070" --domain "amazon.fr" --max 10

# Exemple 3 : Récupérer 20 disques SSD NVMe
python main.py --query "ssd nvme 2to" --max 20
```

### Méthode 3 : Mode Arrière-Plan (Headless)
Pour exécuter le scrapeur en toute discrétion sans afficher la fenêtre Chrome :
```powershell
python main.py --query "smartphone 5g" --max 15 --headless
```

### Méthode 4 : Consulter les Données Déjà Stockées en BDD via la console
```powershell
python main.py --show-db
```

---

## Options Disponibles en Ligne de Commande

| Argument | Description | Exemple |
| :--- | :--- | :--- |
| `--query`, `-q` | Mot-clé technologique à rechercher | `--query "macbook pro m3"` |
| `--max`, `-m` | Nombre maximum de produits à scraper | `--max 20` (défaut : 15) |
| `--domain`, `-d` | Domaine Amazon cible | `--domain "amazon.fr"` (défaut : `amazon.com`) |
| `--category`, `-c` | Nom de la catégorie tech pour la BDD | `--category "PC Portables"` |
| `--headless` | Lance le navigateur Chrome en tâche de fond | `--headless` |
| `--show-db` | Affiche l'historique et les tables en base | `--show-db` |

---

## Architecture MVC

```
SCRAPEUR AMAZONE/
│
├── main.py                   # Point d'entrée principal (CLI interactif ou par arguments)
├── config.py                 # Configuration centralisée (connexion SQL Server SSMS, catégories tech)
├── requirements.txt          # Dépendances (SQLAlchemy, pyodbc, Selenium, BeautifulSoup4)
│
├── models/                   # ── [ MODÈLE (M) ] ──
│   ├── __init__.py
│   ├── database.py           # Moteur SQL Server SQLAlchemy & gestionnaire de transactions
│   └── product.py            # Modèles ORM (Product, ScrapingSession) & DAO (ProductRepository)
│
├── views/                    # ── [ VUE (V) ] ──
│   ├── __init__.py
│   └── cli_view.py           # Présentation Console (bannières, menus, tableaux, stats)
│
├── controllers/              # ── [ CONTRÔLEUR (C) ] ──
│   ├── __init__.py
│   └── scraper_controller.py # Orchestrateur : pilote le scraping, ordonne l'insertion dans SQL Server
│
└── scrapers/                 # ── [ MOTEUR D'EXTRACTION ] ──
    ├── __init__.py
    └── amazon_scraper.py     # Scraper Selenium (undetected-chromedriver) + BeautifulSoup4
```

---

## Schéma des Tables SQL Server (`AmazonTechDB`)

### 1. Table `dbo.scraping_sessions`
Enregistre chaque mission de recherche :
- `id` : Clé primaire auto-incrémentée (IDENTITY)
- `query_text` : Mot-clé recherché (ex: *laptop rtx 4070*, *ssd nvme 2to*)
- `domain` : Domaine Amazon (.com, .fr, etc.)
- `category` : Catégorie technologique ciblée
- `status` : Statut (`running`, `completed`, `error`)
- `started_at` & `completed_at` : Horodatages UTC
- `products_count` : Nombre d'articles collectés

### 2. Table `dbo.products`
Enregistre chaque outil ou produit technologique :
- `id` : Clé primaire auto-incrémentée (IDENTITY)
- `session_id` : Clé étrangère liée à la session
- `asin` : Identifiant Amazon unique
- `title` : Désignation complète du produit tech
- `price_raw`, `price_val`, `currency` : Prix textuel, prix numérique et devise
- `rating_score`, `rating_raw` : Note sur 5
- `reviews_count`, `reviews_raw` : Nombre d'évaluations clients
- `product_url`, `image_url` : Liens web et visuels
- `is_prime`, `is_sponsored`, `badge` : Métadonnées commerciales
- `category`, `domain` : Catégorie et boutique d'origine
- `scraped_at` : Date d'enregistrement
