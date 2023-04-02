import datetime
from sqlalchemy.orm import mapped_column
from .base import Base
from sqlalchemy.orm import Mapped

class Horario(Base):
    __tablename__ = "horarios"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    hora: Mapped[datetime.time]
    dia: Mapped[str]
    