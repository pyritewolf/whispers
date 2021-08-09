from pydantic import SecretStr, validator

from schemas import BaseSchema


class Register(BaseSchema):
    email: str
    password: SecretStr
    username: str
    confirm_password: SecretStr

    @validator("confirm_password")
    def check_if_passwords_match(cls, v, values):
        if v != values["password"]:
            raise ValueError("Passwords don't match, buddy!")
        return v
