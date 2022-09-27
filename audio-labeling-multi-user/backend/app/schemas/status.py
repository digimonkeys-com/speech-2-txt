from pydantic import BaseModel


class Status(BaseModel):
    duration: float
    samples: int
    unrecorded_samples: int
    recorded_samples: int
