from typing import Union, List

from pydantic import BaseModel, conint, constr, validator, field_validator
import re
email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

class NotifyRequest(BaseModel):
    message: constr(max_length=1024)
    recipient: Union[str, List[constr(max_length=150)]]
    delay: conint(ge=0, le=2)

    @field_validator('recipient', mode='before')
    def convert_to_list(cls, v):
        return [v] if isinstance(v, str) else v

    @field_validator('recipient')
    def validate_recipients(cls, v):
        for recipient in v:
            if not (re.fullmatch(email_regex, recipient) or recipient.isdigit()):
                raise ValueError("Invalid recipient format")
        return v
