from pydantic import BaseModel, EmailStr
from typing import Dict, Tuple

class Student(BaseModel):
    name: str
    marks: Dict[str, Tuple[int, int]]  # { "Math": (85, 100), "Science": (90, 100) }
    email: EmailStr  # Ensures valid email format
