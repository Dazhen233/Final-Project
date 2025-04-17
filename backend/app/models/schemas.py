from pydantic import BaseModel

class StoryRequest(BaseModel):
    user_id: str
    character_name: str
    character_source: str
    current_state: str

class InteractionRequest(BaseModel):
    user_id: str
    user_input: str
