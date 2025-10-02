from abc import ABC, abstractmethod
from typing import Type, Optional, Dict, List, Any
from django.db import transaction
from django.db.models import Model, QuerySet
from core.dao import Dao


"""
Module: base_service.py
Author: Imam Hossain Roni
Created: April 01, 2021
Description: ''
Ref: 
    1. https://stackoverflow.com/questions/62740603/how-can-i-implement-service-layer-in-django
    2. https://breadcrumbscollector.tech/how-to-implement-a-service-layer-in-django-rest-framework/
"""


class Service(ABC):
    """
    Abstract base service.
    Each child service must define dao_cls (a DAO class).
    Provides automatic access to dao instance.
    """

    @property
    @abstractmethod
    def dao_cls(self) -> Type[Dao]:
        """Return the DAO class associated with this service"""
        pass

    @property
    def dao(self) -> Dao:
        """Create a DAO instance automatically"""
        return self.dao_cls()


class ReadService(Service, ABC):
    """Base read-only service providing query methods"""

    def get(self, pk: int) -> Optional[Model]:
        """Get object by primary key"""
        return self.dao.get(pk)

    def list_all(self, include_deleted: bool = False) -> QuerySet[Model]:
        """List all objects"""
        return self.dao.all(include_deleted=include_deleted)

    def find_one(self,
                 filter_kwargs: Optional[Dict] = None,
                 exclude_kwargs: Optional[Dict] = None,
                 order_bys: Optional[List[str]] = None) -> Optional[Model]:
        return self.dao.find_one(filter_kwargs, exclude_kwargs, order_bys)

    def find_queryset(self,
                      filter_kwargs: Optional[Dict] = None,
                      exclude_kwargs: Optional[Dict] = None,
                      order_bys: Optional[List[str]] = None) -> QuerySet[Model]:
        return self.dao.find_queryset(filter_kwargs, exclude_kwargs, order_bys)

    def exists(self,
               filter_kwargs: Optional[Dict] = None,
               exclude_kwargs: Optional[Dict] = None) -> bool:
        return self.dao.does_exist(filter_kwargs, exclude_kwargs)

    def count(self,
              filter_kwargs: Optional[Dict] = None,
              exclude_kwargs: Optional[Dict] = None) -> int:
        return self.dao.get_count(filter_kwargs, exclude_kwargs)


class WriteService(Service, ABC):
    """Base write/mutation service"""

    @transaction.atomic
    def create(self, data: Dict[str, Any]) -> Optional[Model]:
        """Create a new object"""
        return self.dao.save(data)

    @transaction.atomic
    def update(self, obj: Model, data: Optional[Dict[str, Any]] = None) -> bool:
        """Update an existing object"""
        if data:
            for key, value in data.items():
                setattr(obj, key, value)
        return self.dao.update(obj)

    @transaction.atomic
    def delete(self, obj: Model) -> bool:
        """Hard delete"""
        return self.dao.delete(obj)

    @transaction.atomic
    def soft_delete(self, obj: Model) -> bool:
        """Soft delete"""
        return self.dao.soft_delete(obj)

    @transaction.atomic
    def create_batch(self, objs: List[Model], batch_size: Optional[int] = None) -> bool:
        """Create multiple objects in bulk"""
        return self.dao.save_batch(objs, batch_size=batch_size)

    @transaction.atomic
    def update_batch(self, objs: List[Model]) -> bool:
        """Update multiple objects"""
        return self.dao.update_batch(objs)

    @transaction.atomic
    def delete_batch(self, objs: List[Model]) -> bool:
        """Delete multiple objects"""
        return self.dao.delete_batch(objs)
