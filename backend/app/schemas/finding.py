from pydantic import BaseModel
from typing import Optional

class FeedbackCreate(BaseModel):
    is_false_positive: bool = True
    comment: Optional[str] = None

class FeedbackResponse(BaseModel):
    id: str
    finding_id: str
    is_false_positive: bool
    comment: Optional[str] = None
    message: str = "Feedback saved successfully."
