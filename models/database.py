"""Couche Modèle : Connexion et gestionnaire de session SQLAlchemy.

Compatible :
- Microsoft SQL Server (SQL Server Management Studio - SSMS)
- SQLite
"""

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
import config

# Configuration des options du moteur selon le type de BDD
engine_kwargs = {"echo": False}
if config.DB_ENGINE_TYPE == "sqlite":
    engine_kwargs["connect_args"] = {"check_same_thread": False}
elif config.DB_ENGINE_TYPE == "mssql":
    engine_kwargs["fast_executemany"] = True

engine = create_engine(config.DATABASE_URI, **engine_kwargs)

# Fabrique de session
SessionFactory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Session = scoped_session(SessionFactory)

# Base déclarative pour les modèles ORM
Base = declarative_base()


def init_db():
    """Crée toutes les tables dans SQL Server (ou SQLite) si elles n'existent pas encore."""
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_db_session():
    """Gestionnaire de contexte pour obtenir une session de base de données sécurisée."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
