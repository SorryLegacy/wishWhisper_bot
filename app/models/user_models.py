from enum import Enum

from sqlalchemy import BigInteger
from sqlalchemy import Enum as EnumDB
from sqlalchemy import ForeignKey, or_, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import AbstarctModel, Base, async_session


class UserMood(Enum):
    SUN = "sun"
    WIND = "wind"
    RAIN = "rain"
    THUNDER = "thunder"
    SNOW = "snow"


class User(AbstarctModel):
    __tablename__ = "user_user"

    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, autoincrement=False)
    mood: Mapped[UserMood] = mapped_column(EnumDB(UserMood), default=UserMood.SUN, nullable=True)

    @hybrid_property
    async def partner(self) -> "User":
        async with async_session() as session:
            partner = await session.execute(
                select(User)
                .join(UserPair, or_(UserPair.second_user_id == User.id, UserPair.main_user_id == User.id))
                .where(
                    or_(UserPair.main_user_id == self.id, UserPair.second_user_id == self.id),
                    User.id != self.id,
                    UserPair.is_approved is True,
                )
            )
            return partner.scalar()

    @hybrid_property
    async def pair(self) -> "UserPair":
        async with async_session() as session:
            pair_corutine = await session.execute(
                select(UserPair).where(or_(UserPair.main_user_id == self.id, UserPair.second_user_id == self.id))
            )
            return pair_corutine.scalar()


class UserPair(Base):
    __tablename__ = "user_pair"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    main_user_id: Mapped[int] = mapped_column(ForeignKey("user_user.id"), nullable=False)
    second_user_id: Mapped[int] = mapped_column(ForeignKey("user_user.id"), nullable=False)
    is_approved: Mapped[bool] = mapped_column(default=False)

    main_user: Mapped[User] = relationship("User", foreign_keys=[main_user_id], uselist=False)
    second_user: Mapped[User] = relationship("User", foreign_keys=[second_user_id], uselist=False)
