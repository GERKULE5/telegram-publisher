from pydantic import BaseModel

class TokenValidationRequest(BaseModel):
    token: str
    platform: str = 'telegram'
    externalUserId: int
    externalChatId: int
