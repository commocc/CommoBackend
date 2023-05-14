from datetime import datetime
from typing import List

from django.db import models
from pydantic import BaseModel


class OrmBaseModel(BaseModel):
    @classmethod
    def from_orms(cls, instances: List[models.Model]):
        return [cls.from_orm(inst) for inst in instances]

    class Config:
        orm_mode = True
