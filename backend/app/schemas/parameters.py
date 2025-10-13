from pydantic import BaseModel

class FrequencyBandParams(BaseModel):
    EDT: float
    T60_from_T20: float
    T60_from_T30: float
    C50: float
    D50: float

class AnalysisResult(BaseModel):
    parameters: dict[str, FrequencyBandParams]