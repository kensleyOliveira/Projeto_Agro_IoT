from dataclasses import dataclass
from datetime import datetime
from domain.exceptions import (
    LeituraIncompletaException,
    TemperaturaInvalidaException,
    UmidadeInvalidaException
)

@dataclass
class LeituraMicroclima:
    temperatura: float
    umidade: float
    timestamp: datetime = None

    def __post_init__(self):
        """
        Validações intrínsecas ao domínio utilizando exceções personalizadas.
        """
        if self.temperatura is None or self.umidade is None:
            raise LeituraIncompletaException()
            
        # Limites operacionais para o sensor no campo
        if not (-20.0 <= self.temperatura <= 80.0):
            raise TemperaturaInvalidaException(self.temperatura)
            
        if not (0.0 <= self.umidade <= 100.0):
            raise UmidadeInvalidaException(self.umidade)
            
        if self.timestamp is None:
            self.timestamp = datetime.now()