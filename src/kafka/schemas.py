from pydantic import BaseModel
from enum import Enum

class MessengerPlatform(Enum):
    TG = 'telegram'
    VK = 'vk'

class TokenValidationRequest(BaseModel):
    token: str
    platform: MessengerPlatform
    externalUserId: int
    externalChatId: int
