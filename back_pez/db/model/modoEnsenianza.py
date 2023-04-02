from sqlalchemy.orm import mapped_column
from .base import Base
from sqlalchemy.orm import Mapped



class ModoEnsenianza(Base):
    __tablename__ = "modosEnsenianza"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    
