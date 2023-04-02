from sqlalchemy.orm import mapped_column
from .base import Base
from sqlalchemy.orm import Mapped

class Competencia(Base):
    __tablename__ = "competencias"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    