"""Couche Modèle : Définition des entités Product et ScrapingSession (SQLAlchemy)."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey, desc, asc, func
)
from sqlalchemy.orm import relationship
from .database import Base, get_db_session


class ScrapingSession(Base):
    """Représente une mission d'extraction de données sur Amazon."""
    __tablename__ = "scraping_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    query_text = Column(String(255), nullable=False)
    domain = Column(String(100), default="amazon.com")
    category = Column(String(100), default="")
    sort_by = Column(String(50), default="relevance")
    max_products = Column(Integer, default=30)
    status = Column(String(20), default="running")  # running, completed, error, stopped
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)
    products_count = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)

    products = relationship("Product", back_populates="session", cascade="all, delete-orphan")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "query": self.query_text,
            "domain": self.domain,
            "category": self.category,
            "sort_by": self.sort_by,
            "max_products": self.max_products,
            "status": self.status,
            "started_at": self.started_at.strftime("%Y-%m-%d %H:%M:%S") if self.started_at else None,
            "completed_at": self.completed_at.strftime("%Y-%m-%d %H:%M:%S") if self.completed_at else None,
            "products_count": self.products_count,
            "error_message": self.error_message,
        }


class Product(Base):
    """Représente un produit ou outil technologique extrait depuis Amazon."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("scraping_sessions.id", ondelete="CASCADE"), nullable=True, index=True)
    asin = Column(String(20), nullable=False, index=True)
    title = Column(Text, nullable=False)
    price_raw = Column(String(50))
    price_val = Column(Float, nullable=True)
    currency = Column(String(10), default="")
    rating_score = Column(Float, nullable=True)
    rating_raw = Column(String(50))
    reviews_count = Column(Integer, nullable=True)
    reviews_raw = Column(String(50))
    product_url = Column(Text)
    image_url = Column(Text)
    is_sponsored = Column(Boolean, default=False)
    is_prime = Column(Boolean, default=False)
    badge = Column(String(100))
    category = Column(String(100))
    domain = Column(String(100))
    scraped_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    session = relationship("ScrapingSession", back_populates="products")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "session_id": self.session_id,
            "asin": self.asin,
            "title": self.title,
            "price_raw": self.price_raw,
            "price_val": self.price_val,
            "currency": self.currency,
            "rating_score": self.rating_score,
            "rating_raw": self.rating_raw,
            "reviews_count": self.reviews_count,
            "reviews_raw": self.reviews_raw,
            "product_url": self.product_url,
            "is_sponsored": self.is_sponsored,
            "is_prime": self.is_prime,
            "badge": self.badge,
            "category": self.category,
            "domain": self.domain,
            "scraped_at": self.scraped_at.strftime("%Y-%m-%d %H:%M:%S") if self.scraped_at else None,
        }


# ── Méthodes DAO / Requêtes du Modèle ──────────────────────────────────────────

class ProductRepository:
    """Couche d'accès aux données (DAO) pour les produits et sessions."""

    @staticmethod
    def create_session(query: str, domain: str, category: str, max_products: int, sort_by: str = "relevance") -> int:
        with get_db_session() as session:
            sess = ScrapingSession(
                query_text=query,
                domain=domain,
                category=category,
                max_products=max_products,
                sort_by=sort_by,
                status="running",
            )
            session.add(sess)
            session.flush()
            return sess.id

    @staticmethod
    def complete_session(session_id: int, products_data: List[Dict[str, Any]], category: str = "", domain: str = ""):
        with get_db_session() as session:
            sess = session.query(ScrapingSession).filter_by(id=session_id).first()
            if sess:
                sess.status = "completed"
                sess.completed_at = datetime.now(timezone.utc)
                sess.products_count = len(products_data)

            for item in products_data:
                prod = Product(
                    session_id=session_id,
                    asin=item.get("asin", ""),
                    title=item.get("title", ""),
                    price_raw=item.get("price_raw", ""),
                    price_val=item.get("price_val"),
                    currency=item.get("currency", ""),
                    rating_score=item.get("rating_score"),
                    rating_raw=item.get("rating_raw", ""),
                    reviews_count=item.get("reviews_count"),
                    reviews_raw=item.get("reviews_raw", ""),
                    product_url=item.get("product_url", ""),
                    image_url=item.get("image_url", ""),
                    is_sponsored=bool(item.get("is_sponsored", False)),
                    is_prime=bool(item.get("is_prime", False)),
                    badge=item.get("badge", ""),
                    category=category,
                    domain=domain,
                )
                session.add(prod)

    @staticmethod
    def fail_session(session_id: int, error_message: str):
        with get_db_session() as session:
            sess = session.query(ScrapingSession).filter_by(id=session_id).first()
            if sess:
                sess.status = "error"
                sess.error_message = error_message
                sess.completed_at = datetime.now(timezone.utc)

    @staticmethod
    def list_products(session_id: Optional[int] = None, search: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        with get_db_session() as session:
            q = session.query(Product)
            if session_id:
                q = q.filter(Product.session_id == session_id)
            if search:
                term = f"%{search}%"
                q = q.filter(Product.title.ilike(term) | Product.asin.ilike(term))
            q = q.order_by(desc(Product.scraped_at)).limit(limit)
            return [p.to_dict() for p in q.all()]

    @staticmethod
    def list_sessions(limit: int = 15) -> List[Dict[str, Any]]:
        with get_db_session() as session:
            sessions = session.query(ScrapingSession).order_by(desc(ScrapingSession.started_at)).limit(limit).all()
            return [s.to_dict() for s in sessions]

    @staticmethod
    def get_database_stats() -> Dict[str, Any]:
        with get_db_session() as session:
            total_products = session.query(func.count(Product.id)).scalar() or 0
            total_sessions = session.query(func.count(ScrapingSession.id)).scalar() or 0
            avg_price = session.query(func.avg(Product.price_val)).scalar()
            avg_rating = session.query(func.avg(Product.rating_score)).scalar()
            total_prime = session.query(func.count(Product.id)).filter(Product.is_prime == True).scalar() or 0
            return {
                "total_products": total_products,
                "total_sessions": total_sessions,
                "avg_price": round(avg_price, 2) if avg_price else 0.0,
                "avg_rating": round(avg_rating, 2) if avg_rating else 0.0,
                "total_prime": total_prime,
            }
