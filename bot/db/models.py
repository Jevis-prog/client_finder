from sqlalchemy import BigInteger, Boolean, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.const import ProcessingStatus
from bot.db.base import Base


class UserModel(Base):
    """Пользователи."""

    __tablename__ = 'users'

    external_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String, nullable=True, default=None)
    profile: Mapped[str] = mapped_column(String, nullable=True)

    messages: Mapped[list['MessageModel']] = relationship(
        back_populates='user', cascade='all, delete-orphan',
    )


class MessageModel(Base):
    """Сообщения."""

    __tablename__ = 'messages'

    sender_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.id'), nullable=False)
    external_id: Mapped[int] = mapped_column(Integer, nullable=False)
    message_text: Mapped[str] = mapped_column(String, nullable=False)
    processing_status: Mapped[ProcessingStatus] = mapped_column(
        Enum(ProcessingStatus), default=ProcessingStatus.PENDING,
    )
    is_lead: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)
    reason: Mapped[str] = mapped_column(String, nullable=True)

    user: Mapped['UserModel'] = relationship(back_populates='messages')
    chat: Mapped['ChatsModel'] = relationship(back_populates='messages')


class ChatsModel(Base):
    """Чаты."""

    __tablename__ = 'chats'

    external_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    chat_title: Mapped[str] = mapped_column(String, nullable=True)

    messages: Mapped[list['MessageModel']] = relationship(
        back_populates='chat', cascade='all, delete-orphan',
    )
