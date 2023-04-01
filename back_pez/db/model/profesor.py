
from sqlalchemy.orm import mapped_column
from .base import Base
from sqlalchemy.orm import Mapped



class Profesor(Base):
    __tablename__ = "profesores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    

