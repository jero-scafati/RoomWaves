from pydantic import BaseModel

class AcousticParameterSet(BaseModel):
    EDT: float
    T60_from_T20: float
    T60_from_T30: float
    C80: float
    D50: float

class AnalysisResult(BaseModel):
    parameters: dict[str, AcousticParameterSet]