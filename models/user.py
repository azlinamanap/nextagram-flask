from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash


class User(BaseModel):
    username = pw.CharField(unique=False)
    password = pw.CharField()
    email = pw.CharField(unique=True)

    def validate(self):
        if len(self.password) < 8:
            self.errors.append('Password must be more than 8 characters')
        else:
            self.password = generate_password_hash(self.password)
