from abc import ABC
from typing import Type

from django.db import models


class ServiceProvider(ABC):
    model: Type[models.Model]
    fields: dict[str:type]

    # override this method
    def __init__(self) -> None:
        pass

    def get_one(self, target_id: int) -> models.Model or None:
        if self.model.objects.filter(id=target_id).exists():
            return self.model.objects.get(id=target_id)
        return None

    def get_list(self) -> list[models.Model]:
        return self.model.objects.all()

    def add_one(self, **kwargs) -> models.Model:
        model = self.model.objects.create(**kwargs)
        return model

    def add_many(self, data: list[dict[str:str]]) -> list[int]:
        result = self.model.objects.bulk_create(data)
        return [model.id for model in result]

    def delete(self, target_id: int) -> bool:
        if self.model.objects.filter(id=target_id).exists():
            self.model.objects.get(id=target_id).delete()
            return True
        return False

    def update(self, target_id: int, **kwargs) -> bool:
        model = self.get_one(target_id)
        if not model:
            return False
        model.update(**kwargs)
        return True
