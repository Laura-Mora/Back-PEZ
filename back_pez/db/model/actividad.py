from sqlalchemy.orm import mapped_column
from .base import Base
from sqlalchemy.orm import Mapped

class Actividad(Base):
    __tablename__ = "actividades"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    