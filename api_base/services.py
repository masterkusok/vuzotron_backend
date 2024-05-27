from abc import ABC
from typing import Type

from django.contrib.postgres.search import SearchVector
from django.db import models
from django.db.models import QuerySet


class ServiceProvider(ABC):
    """
    Base class for model services. This class realizes CRUD operations with db.
    Attributes
    ----------
    model
        The model class
    fields
        Dictionary with model fields names and types. If user
         should be able to work with this field from models
        services,fields dictionary should contain this field
    """

    model: Type[models.Model]
    fields: dict[str:type]

    # override this method
    def __init__(self) -> None:
        pass

    def get_one(self, target_id: int) -> models.Model or None:
        """
        Get specific model from db by its id
        Parameters
        ----------
        target_id: int
            id of target model
        Returns
        -------
        models.Model or None
            Returns None if target_id is not found, otherwise returns target model
        """
        if self.model.objects.filter(id=target_id).exists():
            return self.model.objects.get(id=target_id)
        return None

    def get_list(self, **filters) -> QuerySet:
        """
        Get list of models from db, featuring filters and queries etc.
        Parameters
        ----------
        filters
             filters to be applied. Can be empty to get whole list
        Returns
        -------
        QuerySet
            Result filtered set of models
        """
        if len(filters) == 0:
            return self.model.objects.all()

        vector = SearchVector(*self.fields.keys())
        db_filters = filters
        if "query" in filters:
            db_filters["search__icontains"] = db_filters["query"]
            del db_filters["query"]
        if "page" in filters:
            del db_filters["page"]
        return self.model.objects.annotate(search=vector).filter(**db_filters).all()

    def add_one(self, **kwargs) -> models.Model:
        """
        Add new instance of model to db
        Parameters
        ----------
        kwargs
            fields and their values. All fields should be from fields dict

        Returns
        -------
        models.Model
            Created model
        """
        model = self.model.objects.create(**kwargs)
        return model

    def add_many(self, data: list[dict[str:str]]) -> list[int]:
        """
        Adds list of models to db
        Parameters
        ----------
        data: list[dict[str:str]]
            list of objects to be added to db
        Returns
        -------
        list[int]
            List of ids of new objects
        """
        result = self.model.objects.bulk_create(data)
        return [model.id for model in result]

    def delete(self, target_id: int) -> bool:
        """
        Delete object from db by its id
        Parameters
        ----------
        target_id: int
            id of object to be deleted
        Returns
        -------
        bool
            True if object was successfully deleted, otherwise False
        """
        if self.model.objects.filter(id=target_id).exists():
            self.model.objects.get(id=target_id).delete()
            return True
        return False

    def update(self, target_id: int, **kwargs) -> bool:
        """
        Update data of object, stored in db
        Parameters
        ----------
        target_id:int
            id of object to be updated
        kwargs
            fields and values to be updated. All fields should be in fields dict
        Returns
        -------
        bool
            True if model was successfully updated, otherwise False
        """
        target_model = self.model.objects.filter(id=target_id)
        if not target_model:
            return False
        target_model.update(**kwargs)
        return True
