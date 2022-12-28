from pydantic import BaseModel  # Pydantic BaseModel
# Order class model for request body


class SummarizeRequest(BaseModel):
    url: str
