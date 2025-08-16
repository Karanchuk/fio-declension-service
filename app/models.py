from pydantic import BaseModel

class DeclensionRequest(BaseModel):
    fio: str   # строка, например "Иванов Иван Иванович"
    case: str  # "nomn", "gent", "datv", "accs", "ablt", "loct"

class DeclensionResponse(BaseModel):
    original: str
    case: str
    declined: str
