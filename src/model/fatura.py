from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid

@dataclass
class Fatura:
    Chave: Optional[str] = str(uuid.uuid4())
    Empresa: Optional[str] = None
    Cliente: Optional[str] = None
    Vencimento: Optional[str] = None
    MesRef: Optional[str] = None
    MesEmis: Optional[str] = None
    Valor: Optional[str] = None
    Situacao: Optional[str] = None
    LeituraAnter: Optional[str] = None
    LeituraAtual: Optional[str] = None
    LeituraProxi: Optional[str] = None
    NumDias: Optional[str] = None
    EnergiaInjetada: Optional[str] = None
    ConsumoAtivoNaPonta: Optional[str] = None
    ConsumoAtivoForaDaPonta: Optional[str] = None
    ConsumoTUSDNPonta: Optional[str] = None
    ConsumoTUSDFPonta: Optional[str] = None
    TaxaColetaLixo: Optional[str] = None
    ConservacaoHidrometro: Optional[str] = None
    MetroCubicos: Optional[str] = None
    Cancelado: Optional[bool] = False
    Arquivo: Optional[str] = None
    Base64File: Optional[str] = None
    Criado: Optional[datetime] = datetime.now()
