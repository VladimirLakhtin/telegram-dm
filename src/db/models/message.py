"""Message model file"""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Message(Base):
    """Mailing messages model."""

    title: Mapped[str] = mapped_column(String(50))
    """ Message title"""
    text: Mapped[str]
    """ Message title"""

    def __str__(self):
        return f'{self.__class__.__name__}(title={self.title})'

    def __repr__(self):
        return str(self)