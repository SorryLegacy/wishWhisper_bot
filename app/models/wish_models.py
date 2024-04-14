from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base
from .user_models import User


class Wish(Base):
    __tablename__ = "wish_wish"

    id: Mapped[int] = mapped_column(BigInteger, autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=True)
    prioritet: Mapped[int] = mapped_column(BigInteger, default=5)

    user_id: Mapped[int] = mapped_column(ForeignKey("user_user.id"))
    user: Mapped[User] = relationship("User", backref="wishes")
