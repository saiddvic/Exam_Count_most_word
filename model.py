from sqlalchemy import BigInteger, TEXT
from sqlalchemy.orm import mapped_column, Mapped

from base import CreateModel

class Order(CreateModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    word: Mapped[str] = mapped_column(TEXT)
    counter: Mapped[int] = mapped_column(BigInteger)
