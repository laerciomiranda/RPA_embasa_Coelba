from dataclasses import dataclass

@dataclass
class PdfModel:
    MesRef: str     = ""
    MesEmis: str    = ""
    Vencimento: str = ""
    Valor:str       = ""
    LeituraAnt:str  = ""
    LeituraAtu:str  = ""
    leituraPro:str  = ""
    NumDias:str     = ""
    Energiainj:str  = ""
    consumoNap:str  = ""
    ConsumoFop:str  = ""
    ConsumoAnp:str  = ""
    ConsumoAfp:str  = ""
    tcl:str  = ""
    hidrometro:str  = ""
    m3:str  = ""