# Add your DAO code here
from core.dao import Dao
from .models import User


class UserDAO(Dao):
    @property
    def model_cls(self):
        return User
