from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey


class Sentence(Base):
    __tablename__ = "sentences"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    text_id: Mapped[int] = mapped_column(ForeignKey("texts.id", ondelete="CASCADE"))
    index: Mapped[int]
    content: Mapped[str]
