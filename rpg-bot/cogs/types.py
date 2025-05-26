from typing import TypedDict, List, Dict, Any, Union

class Config(TypedDict):
    token: str
    prefix: str
    master_id: str
    channel_category: str

class Efeito(TypedDict):
    nome: str
    tipo: int
    alvo: List[str]
    valor: Union[float, List[Union[List[Union[str, float]], float]]]

class DadosFicha(TypedDict):
    exp: int
    multiplicador_nivel: float
    atributos: Dict[str, int]
    multiplicadores: Dict[str, float]
    flat: Dict[str, int]
    efeitos: List[Efeito]
    habilidades: Dict[str, Any]
    inventario: Dict[str, List[str]]

class Ficha(TypedDict):
    id: str
    nome: str
    idade: int
    raca: str
    classe: str
    permissoes: List[str]
    channel_id: str
    dados: DadosFicha

class Recursos(TypedDict):
    vida: Dict[str, float]
    mana: Dict[str, float]
    aura: Dict[str, float]