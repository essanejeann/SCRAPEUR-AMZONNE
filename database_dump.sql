-- ==============================================================
-- DUMP SQL SERVER : Base de données AmazonTechDB
-- Projet : Amazon Tech Scraper (Architecture MVC)
-- Fichier consultable directement par le professeur sur GitHub
-- ==============================================================

IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'AmazonTechDB')
    CREATE DATABASE AmazonTechDB;
GO
USE AmazonTechDB;
GO

IF OBJECT_ID('dbo.products', 'U') IS NOT NULL DROP TABLE dbo.products;
IF OBJECT_ID('dbo.scraping_sessions', 'U') IS NOT NULL DROP TABLE dbo.scraping_sessions;
GO

CREATE TABLE dbo.scraping_sessions (
    id INT IDENTITY(1,1) PRIMARY KEY,
    query_text NVARCHAR(255) NOT NULL,
    domain NVARCHAR(100) DEFAULT 'amazon.com',
    category NVARCHAR(100) DEFAULT '',
    status NVARCHAR(20) DEFAULT 'completed',
    started_at DATETIME DEFAULT GETDATE(),
    products_count INT DEFAULT 0
);
GO

CREATE TABLE dbo.products (
    id INT IDENTITY(1,1) PRIMARY KEY,
    session_id INT FOREIGN KEY REFERENCES dbo.scraping_sessions(id),
    asin NVARCHAR(20) NOT NULL,
    title NVARCHAR(MAX) NOT NULL,
    price_raw NVARCHAR(50),
    price_val FLOAT,
    currency NVARCHAR(10),
    rating_score FLOAT,
    reviews_count INT,
    is_prime BIT DEFAULT 0,
    category NVARCHAR(100),
    domain NVARCHAR(100),
    scraped_at DATETIME DEFAULT GETDATE()
);
GO

SET IDENTITY_INSERT dbo.scraping_sessions ON;
INSERT INTO dbo.scraping_sessions (id, query_text, domain, category, status, products_count) VALUES (1, N'laptop ordinateur portable', N'amazon.fr', N'Laptops & PC Portables', N'completed', 15);
SET IDENTITY_INSERT dbo.scraping_sessions OFF;
GO

SET IDENTITY_INSERT dbo.products ON;
INSERT INTO dbo.products (id, session_id, asin, title, price_raw, price_val, currency, rating_score, reviews_count, is_prime, category, domain) VALUES (1, 1, N'B0DY2T14P6', N'HP 15-fd0001sf Ordinateur Portable 15,6" FHD, PC Portable (Intel Celeron N100, RAM 4 Go, UFS 128 Go, Intel UHD Graphic, Windows 11), Laptop Argent, Clavier AZERTY', N'289,00 €', 289.0, N'€', 4.2, 175, 0, N'Laptops & PC Portables', N'amazon.fr');
INSERT INTO dbo.products (id, session_id, asin, title, price_raw, price_val, currency, rating_score, reviews_count, is_prime, category, domain) VALUES (2, 1, N'B0HG52H23H', N'Ordinateur Portable Win 11 Laptop,15,6" PC Portable Pas Cher Laptop Clavier anglais, film silicone AZERTY, et 1 an d''Office 365 gratuit, 5205U, 4 Go RAM 128 Go ROM Extensible TF 512Go', N'219,99 €', 219.99, N'€', 4.6, 5, 0, N'Laptops & PC Portables', N'amazon.fr');
INSERT INTO dbo.products (id, session_id, asin, title, price_raw, price_val, currency, rating_score, reviews_count, is_prime, category, domain) VALUES (3, 1, N'B0GQJ8TY68', N'ASUS CM1505CM4A-S70121 15.6 Pouces FHD (1920 x 1080) 60Hz Pc Portable (processeur MediaTek Kompanio 540 jusqu''à 2.6GHz, 8Go LPDDR5X, 128Go eMMC) ChromeOS – Clavier AZERTY - sans Chargeur', N'249,99 €', 249.99, N'€', 4.0, 97, 0, N'Laptops & PC Portables', N'amazon.fr');
INSERT INTO dbo.products (id, session_id, asin, title, price_raw, price_val, currency, rating_score, reviews_count, is_prime, category, domain) VALUES (4, 1, N'B0HKHVKM2S', N'Ordinateur Portable 15,6 Pouces IPS FHD, Core i3-6100U, 8Go RAM 256Go SSD PC Portable avec Clavier Rétroéclairé, Pavé Numérique, Déverrouillage par Empreinte, Caméra, HDMI, Type-C, USB 3.0*2', N'299,99 €', 299.99, N'€', 5.0, 12, 0, N'Laptops & PC Portables', N'amazon.fr');
INSERT INTO dbo.products (id, session_id, asin, title, price_raw, price_val, currency, rating_score, reviews_count, is_prime, category, domain) VALUES (5, 1, N'B0B8QYXY9H', N'Acer Aspire Go 17 | PC Portable | 17.3" | Intel N150 | 8Go | 128 Go 17.3" FHD 60 Hz | Intel N150 | 8Go RAM | 128Go UFS | Windows 11 Home | Clavier FR AZERTY | Adaptateur inclus', N'419,00 €', 419.0, N'€', 4.2, 59, 0, N'Laptops & PC Portables', N'amazon.fr');
INSERT INTO dbo.products (id, session_id, asin, title, price_raw, price_val, currency, rating_score, reviews_count, is_prime, category, domain) VALUES (6, 1, N'B0CPJNNLR4', N'Lenovo (FullHD 15,6 Zoll Ordinateur Portable Gaming (AMD® Ryzen5 7520U 8 Threads, 4.30 GHz, 16Go DDR5, 512 Go SSD, Radeon™ 610M, HDMI, BT, USB 3.0, Cam, Windows 11, Clavier AZERTY [français]) #7467', N'549,00 €', 549.0, N'€', 4.3, 126, 0, N'Laptops & PC Portables', N'amazon.fr');
INSERT INTO dbo.products (id, session_id, asin, title, price_raw, price_val, currency, rating_score, reviews_count, is_prime, category, domain) VALUES (7, 1, N'B0H11DFC26', N'2026 Ordinateur Portable 14 Pouces N4020(jusqu''à 2,9 GHz) 8Go DDR4 Win11 256Go SSD Extension 1To 5G WiFi HDMl FHD PC Portable avec Souris sans Fil qwerty Clavier AZERTY Membrane du Clavier- Gris', N'249,99 €', 249.99, N'€', 4.4, 63, 0, N'Laptops & PC Portables', N'amazon.fr');
INSERT INTO dbo.products (id, session_id, asin, title, price_raw, price_val, currency, rating_score, reviews_count, is_prime, category, domain) VALUES (8, 1, N'B0HFZ78WPC', N'Ordinateur Portable 16 " Core i3-1000NG4 (jusqu''à 3,2 GHz),16+512Go SSD Soutien Extension 1TB ,PC Portable Win11 Avec Double WIFI 1920x1200 BT4.2 Souris sans Fil&AZERTY Clavier Couverture-Argent-2', N'369,99 €', 369.99, N'€', 5.0, 1, 0, N'Laptops & PC Portables', N'amazon.fr');
INSERT INTO dbo.products (id, session_id, asin, title, price_raw, price_val, currency, rating_score, reviews_count, is_prime, category, domain) VALUES (9, 1, N'B0FXRFG5B8', N'Ordinateur Portable 14 Pouces Celeron N5095(jusqu''à 2,9 GHz)8Go RAM Win11 256Go SSD Extension1To 5G WiFi 1920x1080FHD PC Portable avec Souris sans Fil qwerty Clavier AZERTY Membranedu Clavier-Violet13', N'279,99 €', 279.99, N'€', 4.1, 51, 0, N'Laptops & PC Portables', N'amazon.fr');
INSERT INTO dbo.products (id, session_id, asin, title, price_raw, price_val, currency, rating_score, reviews_count, is_prime, category, domain) VALUES (10, 1, N'B0GX64X14Q', N'Lenovo Chrome | Laptop | Kompanio 540 | 8Go | 128 Go | Sans chargeur 14'''' IPS MediaTek Kompanio 540 8Go RAM Go 128 Go SSD Arm Mali-G57 MC2 GPU ChromeOS Clavier AZERTY français non rétroélairé', N'299,99 €', 299.99, N'€', 5.0, 1, 0, N'Laptops & PC Portables', N'amazon.fr');
INSERT INTO dbo.products (id, session_id, asin, title, price_raw, price_val, currency, rating_score, reviews_count, is_prime, category, domain) VALUES (11, 1, N'B0H6M57QGJ', N'PINSTONE PC Portable de 14 Pouces Celeron N4000 (jusqu''à 2,6 GHz) 6GB RAM 128GB SSD, Laptop Computer Support WiFi 2.4 / 5G, Bluetooth 5.0, Ordinateur Portable étudiant/Bureau avec Souris.', N'', NULL, N'', 4.0, 15, 0, N'Laptops & PC Portables', N'amazon.fr');
INSERT INTO dbo.products (id, session_id, asin, title, price_raw, price_val, currency, rating_score, reviews_count, is_prime, category, domain) VALUES (12, 1, N'B0BBKYTKXR', N'Acer Chromebook Plus 514 I 14" WUXGA | Core 3 | 8Go | 128Go | ChromeOS 14" IPS WUXGA | Intel Core 3 N355 | 8Go RAM | 128Go eMMC | Clavier FR AZERTY | ChromeOS | Alimentation incluse', N'359,00 €', 359.0, N'€', 4.3, 24, 0, N'Laptops & PC Portables', N'amazon.fr');
INSERT INTO dbo.products (id, session_id, asin, title, price_raw, price_val, currency, rating_score, reviews_count, is_prime, category, domain) VALUES (13, 1, N'B0H3F32J2S', N'Ordinateur Portable 15,6 Pouces 8 Go RAM,SSD 256 Go,processeur N4000 Win 11, PC Portable Wi-FI 5 Double Bande,Bluetooth 4.2, USB-A, HDMI, écran FHD 1920 x 1080 (8, GB)', N'218,49 €', 218.49, N'€', 3.0, 23, 0, N'Laptops & PC Portables', N'amazon.fr');
INSERT INTO dbo.products (id, session_id, asin, title, price_raw, price_val, currency, rating_score, reviews_count, is_prime, category, domain) VALUES (14, 1, N'B0HFWTZ59X', N'Lenovo IdeaPad Slim 3 | Laptop | R3 | 8Go | 512GB | Chargeur Non Inclus 15.6" FHD, 8Go RAM, 512Go SSD, Windows 11 Home, Clavier AZERTY français non rétroélairé', N'499,99 €', 499.99, N'€', 4.0, 1, 0, N'Laptops & PC Portables', N'amazon.fr');
INSERT INTO dbo.products (id, session_id, asin, title, price_raw, price_val, currency, rating_score, reviews_count, is_prime, category, domain) VALUES (15, 1, N'B0FXRDG7P5', N'Ordinateur Portable 14 Pouces Celeron N5095 (jusqu''à 2,9 GHz) Win11 8Go 256Go SSD Extension 1To 5G WiFi FHD HDMl PC Portable avec Souris sans Fil qwerty Clavier avec AZERTY Membrane Clavier - Noir-11', N'279,99 €', 279.99, N'€', 4.1, 51, 0, N'Laptops & PC Portables', N'amazon.fr');
SET IDENTITY_INSERT dbo.products OFF;
GO
