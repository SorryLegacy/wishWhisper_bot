from enum import Enum

from sqlalchemy import BigInteger, ForeignKey, select, or_, Enum as EnumDB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from .database import Base, AbstarctModel, async_session


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

    # # Создаем два relationship для связи с таблицей UserRelation
    # main_user: Mapped["UserPair"] = relationship(
    #     "UserPair",
    #     back_populates="pair",
    #     foreign_keys="UserPair.main_user_id",
    #     uselist=False,  # Указываем, что связь один-к-одному
    #     lazy='selectin'

    # )
    # second_user: Mapped["UserPair"] = relationship(
    #     "UserPair",
    #     back_populates="pair",
    #     foreign_keys="UserPair.second_user_id",
    #     uselist=False,  # Указываем, что связь один-к-одному
    #     lazy='selectin'
    # )

    @hybrid_property
    async def partner(self) -> "User":
        async with async_session() as session:
            partner = await session.execute(
                select(User)
                .join(UserPair, or_(UserPair.second_user_id == User.id, UserPair.main_user_id == User.id))
                .where(or_(UserPair.main_user_id == self.id, UserPair.second_user_id == self.id), User.id != self.id)
            )
            return partner.scalar()

    @hybrid_property
    async def pair(self) -> "UserPair":
        async with async_session() as session:
            pair_corutine = await session.execute(
                select(UserPair).where(or_(UserPair.main_user_id == self.id, UserPair.second_user_id == self.id))
            )
            return pair_corutine.scalar()

    # @property
    # async def has_pair(self) -> bool:
    #     # TODO check is_approved?
    #     if any((self.main_user, self.second_user)):
    #         return True
    #     return False


class UserPair(Base):
    __tablename__ = "user_pair"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    main_user_id: Mapped[int] = mapped_column(ForeignKey("user_user.id"), nullable=False)
    second_user_id: Mapped[int] = mapped_column(ForeignKey("user_user.id"), nullable=False)
    is_approved: Mapped[bool] = mapped_column(default=False)

    main_user: Mapped[User] = relationship("User", foreign_keys=[main_user_id], uselist=False)
    second_user: Mapped[User] = relationship("User", foreign_keys=[second_user_id], uselist=False)
