# Amazon Tech Scraper — Architecture MVC & SQL Server (SSMS)

### Informations du Projet
- **Étudiant :** ESSANE Jean-Noël
- **Niveau :** Licence 2 (L2) — Génie Logiciel
- **Matière / Module :** Programmation & Gestion des Bases de Données
- **Architecture :** Modèle - Vue - Contrôleur (MVC)
- **SGBD :** Microsoft SQL Server (SQL Server Management Studio - SSMS)

---

## Présentation du Projet

Ce projet implémente un système complet d'extraction et de gestion de données (Web Scraping) ciblant les outils et matériels technologiques sur Amazon (ordinateurs portables, composants, accessoires connectés).

L'application est conçue selon les principes du génie logiciel :
- **Architecture MVC (Modèle-Vue-Contrôleur)** stricte et modulaire.
- **Persistance des données** dans un SGBD relationnel professionnel : **Microsoft SQL Server (SSMS)** avec SQLAlchemy et ODBC.
- **Application console autonome** : extraction, structuration et insertion automatique en base de données sans dépendance à une interface web superflue.

---

## Aperçu des Données Extraites en Base de Données

Toutes les données ci-dessous proviennent directement de la base **`AmazonTechDB`** :

1. **Script SQL complet de la base :** [`database_dump.sql`](database_dump.sql) *(contient le schéma DDL et les instructions INSERT des 15 articles technologiques)*.
2. **Tableau des articles technologiques enregistrés dans SQL Server :**

| # | ASIN | Prix | Note | Avis | Modèle & Caractéristiques Techniques |
| :-: | :---: | :---: | :---: | :---: | :--- |
| **1** | `B0DY2T14P6` | 289.00 € | 4.2 / 5 | 175 | **HP 15-fd0001sf Ordinateur Portable 15,6" FHD** |
| **2** | `B0HG52H23H` | 219.99 € | 4.6 / 5 | 5 | **Ordinateur Portable Win 11 Laptop, 15,6" PC Portable** |
| **3** | `B0GQJ8TY68` | 249.99 € | 4.0 / 5 | 97 | **ASUS CM1505CM4A-S70121 15.6 Pouces FHD (1920 x 1080)** |
| **4** | `B0HKHVKM2S` | 299.99 € | 5.0 / 5 | 12 | **Ordinateur Portable 15,6 Pouces IPS FHD, Core i3** |
| **5** | `B0B8QYXY9H` | 419.00 € | 4.2 / 5 | 59 | **Acer Aspire Go 17 \| PC Portable \| 17.3" \| Intel** |
| **6** | `B0CPJNNLR4` | 549.00 € | 4.3 / 5 | 126 | **Lenovo FullHD 15,6 Ordinateur Portable Gaming** |
| **7** | `B0H11DFC26` | 249.99 € | 4.4 / 5 | 63 | **Ordinateur Portable 14 Pouces N4020 SSD** |
| **8** | `B0HFZ78WPC` | 369.99 € | 5.0 / 5 | 1 | **Ordinateur Portable 16" Core i3-1000NG4** |
| **9** | `B0FXRFG5B8` | 279.99 € | 4.1 / 5 | 51 | **Ordinateur Portable 14 Pouces Celeron N5095** |
| **10** | `B0GX64X14Q` | 299.99 € | 5.0 / 5 | 1 | **Lenovo Chrome \| Laptop \| Kompanio 540 \| 8Go** |
| **11** | `B0H6M57QGJ` | - | 4.0 / 5 | 15 | **PINSTONE PC Portable de 14 Pouces Celeron N4000** |
| **12** | `B0BBKYTKXR` | 359.00 € | 4.3 / 5 | 24 | **Acer Chromebook Plus 514 \| 14" WUXGA \| Core 3** |
| **13** | `B0H3F32J2S` | 218.49 € | 3.0 / 5 | 23 | **Ordinateur Portable 15,6 Pouces 8 Go RAM, SSD 256** |
| **14** | `B0HFWTZ59X` | 499.99 € | 4.0 / 5 | 1 | **Lenovo IdeaPad Slim 3 \| Laptop \| R3 \| 8Go \| 512GB** |
| **15** | `B0FXRDG7P5` | 279.99 € | 4.1 / 5 | 51 | **Ordinateur Portable 14 Pouces Celeron N5095** |

---

## Visualisation dans SQL Server Management Studio (SSMS)

Les données sont enregistrées dans la base **`AmazonTechDB`** de votre serveur local SQL Server.

### 1. Connexion à SSMS
1. Lancez **SQL Server Management Studio**.
2. Connectez-vous avec :
   - **Nom du serveur :** `localhost` (ou `.`)
   - **Authentification :** Authentification Windows
3. Cliquez sur **Se connecter**.

### 2. Emplacement des Données
Dans l'Explorateur d'objets :
- **`AmazonTechDB` > Tables > `dbo.products`** : Données des produits technologiques (titre, prix, note, avis, ASIN, URL).
- **`AmazonTechDB` > Tables > `dbo.scraping_sessions`** : Historique des sessions de scraping.

### 3. Requêtes SQL
Ouvrez une **Nouvelle Requête** et exécutez (`F5`) :

```sql
USE AmazonTechDB;
GO

-- 1. Lister tous les produits technologiques
SELECT id, asin, title, price_raw, rating_score, reviews_count 
FROM products;

-- 2. Trier les produits par note décroissante
SELECT title, price_raw, rating_score 
FROM products 
ORDER BY rating_score DESC;

-- 3. Consulter les sessions de scraping exécutées
SELECT id, query_text, started_at, status, products_count 
FROM scraping_sessions;
```

---

## Instructions d'Exécution du Scrapeur

### Étape 1 : Activer l'environnement Python
Dans le terminal PowerShell :
```powershell
cd "c:\Users\PC\Desktop\repertoi iit\SCRAPEUR AMAZONE"
.\.venv\Scripts\Activate.ps1
```

### Étape 2 : Installer les dépendances (si nécessaire)
```powershell
pip install -r requirements.txt
```

### Étape 3 : Lancer le programme

- **Mode Interactif (Menu guidé avec choix des catégories tech) :**
  ```powershell
  python main.py
  ```

- **Mode Commande Directe :**
  ```powershell
  # Scraper 15 ordinateurs portables
  python main.py --query "laptop dell" --max 15

  # Scraper des cartes graphiques
  python main.py --query "carte graphique RTX 4070" --domain "amazon.fr" --max 10
  ```

- **Consulter le contenu de la base sans relancer de scraping :**
  ```powershell
  python main.py --show-db
  ```

---

## Architecture MVC du Projet

```
SCRAPEUR AMAZONE/
│
├── main.py                   # Point d'entrée principal (CLI interactif & paramètres)
├── config.py                 # Configuration centralisée (SGBD SQL Server, catégories)
├── database_dump.sql         # Export SQL complet pour évaluation directe
├── requirements.txt          # Dépendances du projet (SQLAlchemy, pyodbc, Selenium, etc.)
│
├── models/                   # ── [ MODÈLE (M) ] ──
│   ├── database.py           # Gestion de la connexion SQL Server & sessions SQLAlchemy
│   └── product.py            # Classes Product & ScrapingSession + DAO ProductRepository
│
├── views/                    # ── [ VUE (V) ] ──
│   └── cli_view.py           # Présentation console (tableaux formatés, progression, stats)
│
├── controllers/              # ── [ CONTRÔLEUR (C) ] ──
│   └── scraper_controller.py # Logique métier : orchestre le scraping et persiste en BDD
│
└── scrapers/                 # ── [ MOTEUR D'EXTRACTION ] ──
    └── amazon_scraper.py     # Module d'extraction Selenium & BeautifulSoup
```

---

## Schéma Relationnel des Tables

### 1. Table `dbo.scraping_sessions`
- `id` : Identifiant unique auto-incrémenté (PRIMARY KEY)
- `query_text` : Mot-clé recherché
- `domain` : Domaine Amazon (.com, .fr, etc.)
- `category` : Catégorie technologique ciblée
- `status` : Statut d'exécution (`completed`, `error`)
- `started_at` : Date et heure de début
- `completed_at` : Date et heure de fin
- `products_count` : Nombre d'articles collectés

### 2. Table `dbo.products`
- `id` : Identifiant unique auto-incrémenté (PRIMARY KEY)
- `session_id` : Référence vers la session de scraping (FOREIGN KEY)
- `asin` : Identifiant standard Amazon (ASIN)
- `title` : Titre complet et caractéristiques du produit
- `price_raw`, `price_val`, `currency` : Prix brut, valeur numérique et devise
- `rating_score`, `rating_raw` : Note sur 5
- `reviews_count` : Nombre d'avis clients
- `product_url`, `image_url` : Liens web et visuels
- `category`, `domain` : Catégorie et plateforme d'origine
- `scraped_at` : Horodatage de l'enregistrement
