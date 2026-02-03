from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime


class Base(DeclarativeBase):
    pass

class BlockedDomain(Base):
    @staticmethod
    def normalise_domain(raw: str) -> str:
        domain = raw.strip().lower()
        if domain == "":
            raise ValueError("No string provided.")
        elif domain.endswith("."):
            domain = domain[:-1]
        return domain

    @classmethod
    def create(cls, domain: str) -> "BlockedDomain":
        return cls(domain=cls.normalise_domain(domain))

    __tablename__ = "blocked_domains"

    domain: Mapped[str] = mapped_column(primary_key=True)
    enabled: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)