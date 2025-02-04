from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from .models import Message, Base
from .database import engine, get_db
from .tasks import send_notification
import os
from dotenv import load_dotenv
from pydantic import BaseModel, validator
from typing import List, Union

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI()

class NotifyRequest(BaseModel):
    message: str
    recipient: Union[List[str], str]
    delay: int

    @validator('recipient', pre=True)
    def convert_to_list(cls, v):
        if isinstance(v, str):
            return [v]
        return v

DELAY_MAPPING = {0: 0, 1: 3600, 2: 86400}

@app.post("/api/notify/")
async def notify(
        request: NotifyRequest,
        db: Session = Depends(get_db)
):
    message = Message(content=request.message)
    db.add(message)
    db.commit()
    db.refresh(message)
    for recipient in request.recipient:
        recipient_type = (
            "email"
            if "@" in recipient
            else "telegram"
        )
        send_notification.apply_async(
            args=[message.id, recipient, recipient_type],
            countdown=DELAY_MAPPING[request.delay]
        )
    return {"status": "Notifications scheduled"}
