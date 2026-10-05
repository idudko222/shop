from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class WalletModel(Base):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    amount: Mapped[float] = mapped_column(Float, default=0)
