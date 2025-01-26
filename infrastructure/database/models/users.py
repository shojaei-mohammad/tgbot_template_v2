from typing import Optional

from sqlalchemy import Integer, BigInteger, String
from sqlalchemy.orm import mapped_column, Mapped
from typing_extensions import Annotated

from .base import TimestampMixin, TableNameMixin, Base

str_255 = Annotated[str, mapped_column(String(255), nullable=True)]


class BotUser(Base, TimestampMixin, TableNameMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, index=True, unique=True
    )
    name: Mapped[Optional[str_255]]
    lastname: Mapped[Optional[str_255]]
    username: Mapped[Optional[str_255]]
    referral_code: Mapped[int] = mapped_column(BigInteger, nullable=True)
    referred_by: Mapped[int] = mapped_column(BigInteger, nullable=True)
    referral_count: Mapped[int] = mapped_column(Integer, default=0)
    referral_link: Mapped[str_255]
    pref_language: Mapped[str_255]

    def __repr__(self):
        return f"<User {self.id} {self.ChatID} {self.Username}>"
