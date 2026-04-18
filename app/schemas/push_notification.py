from pydantic import BaseModel, Field


class PushTokenRegisterRequest(BaseModel):
    fcm_token: str = Field(..., min_length=20, max_length=512)


class PushPreferenceUpdateRequest(BaseModel):
    enabled: bool


class PushNotificationStatusResponse(BaseModel):
    push_enabled: bool
    token_registered: bool
