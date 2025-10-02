import functools
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Type, Any
from django.db.models import Model, QuerySet
from django.utils.functional import cached_property

"""
Module: base_dao.py
Author: Imam Hossain Roni
Created: April 01, 2021

Description: ''
Ref:
    1. https://en.wikipedia.org/wiki/Data_access_object
    2. https://hosseinnejati.medium.com/what-is-dao-understanding-the-data-access-object-pattern-6f5f7af77c36
"""


class Dao(ABC):
    """
    Base DAO class for Django ORM.

    Provides standard CRUD operations, batch operations,
    soft-delete, and flexible query methods.
    """

    SAVE_BATCH_SIZE = 1000
    VALIDATOR_CLASS = None

    @property
    @abstractmethod
    def model_cls(self) -> Type[Model]:
        """Override in child DAO with Django model class"""
        pass

    @cached_property
    def model(self) -> Type[Model]:
        """Cached access to model_cls"""
        return self.model_cls

    def get(self, pk: int) -> Optional[Model]:
        if not pk:
            return None
        return self.model_cls.objects.filter(id=pk).first()

    def all(self, include_deleted: bool = False) -> QuerySet[Model]:
        qs = self.model.objects.all()
        if hasattr(self.model, 'is_deleted') and not include_deleted:
            qs = qs.filter(is_deleted=False)
        return qs

    def save(self, data: Dict[str, Any]) -> Optional[Model]:
        """Insert one object"""
        if not data:
            return None
        obj = self.model_cls(**data)
        obj.save()
        return obj

    def save_batch(self, objs: List[Model], batch_size: Optional[int] = None) -> bool:
        """Insert multiple objects"""
        if not objs:
            return False
        batch_size = batch_size or self.SAVE_BATCH_SIZE
        self.model.objects.bulk_create(objs, batch_size=batch_size)
        return True

    def update(self, obj: Optional[Model]) -> bool:
        if not obj:
            return False
        obj.save()
        return True

    def update_batch(self, objs: List[Model]) -> bool:
        if not objs:
            return False
        for obj in objs:
            self.update(obj)
        return True

    def update_batch_by_query(self, query_kwargs: Dict[str, Any], exclude_kwargs: Dict[str, Any],
                              new_kwargs: Dict[str, Any]) -> bool:
        self.model.objects.filter(**query_kwargs).exclude(**exclude_kwargs).update(**new_kwargs)
        return True

    def delete(self, obj: Optional[Model]) -> bool:
        if not obj:
            return False
        obj.delete()
        return True

    def delete_batch(self, objs: List[Model]) -> bool:
        if not objs:
            return False
        for obj in objs:
            self.delete(obj)
        return True

    def delete_batch_by_query(self, filter_kwargs: Dict[str, Any], exclude_kwargs: Dict[str, Any] = None) -> bool:
        qs = self.model.objects.filter(**filter_kwargs)
        if exclude_kwargs:
            qs = qs.exclude(**exclude_kwargs)
        qs.delete()
        return True

    def soft_delete(self, obj: Optional[Model]) -> bool:
        """Soft-delete (requires model to have 'is_deleted' boolean field)"""
        if not obj or not hasattr(obj, 'is_deleted'):
            return False
        obj.is_deleted = True
        obj.save()
        return True

    def find_one(self,
                 filter_kwargs: Optional[Dict[str, Any]] = None,
                 exclude_kwargs: Optional[Dict[str, Any]] = None,
                 order_bys: Optional[List[str]] = None) -> Optional[Model]:
        qs = self.model.objects.all()
        if filter_kwargs:
            qs = qs.filter(**filter_kwargs)
        if exclude_kwargs:
            qs = qs.exclude(**exclude_kwargs)
        if order_bys:
            qs = qs.order_by(*order_bys)
        return qs.first()

    def find_queryset(self,
                      filter_kwargs: Optional[Dict[str, Any]] = None,
                      exclude_kwargs: Optional[Dict[str, Any]] = None,
                      order_bys: Optional[List[str]] = None) -> QuerySet[Model]:
        qs = self.model.objects.all()
        if filter_kwargs:
            qs = qs.filter(**filter_kwargs)
        if exclude_kwargs:
            qs = qs.exclude(**exclude_kwargs)
        if order_bys:
            qs = qs.order_by(*order_bys)
        return qs

    def find_all_model_objs(self,
                            filter_kwargs: Optional[Dict[str, Any]] = None,
                            exclude_kwargs: Optional[Dict[str, Any]] = None,
                            order_bys: Optional[List[str]] = None) -> List[Model]:
        return list(self.find_queryset(filter_kwargs, exclude_kwargs, order_bys))

    def does_exist(self,
                   filter_kwargs: Optional[Dict[str, Any]] = None,
                   exclude_kwargs: Optional[Dict[str, Any]] = None) -> bool:
        qs = self.model.objects.all()
        if filter_kwargs:
            qs = qs.filter(**filter_kwargs)
        if exclude_kwargs:
            qs = qs.exclude(**exclude_kwargs)
        return qs.exists()

    def get_count(self,
                  filter_kwargs: Optional[Dict[str, Any]] = None,
                  exclude_kwargs: Optional[Dict[str, Any]] = None) -> int:
        qs = self.model.objects.all()
        if filter_kwargs:
            qs = qs.filter(**filter_kwargs)
        if exclude_kwargs:
            qs = qs.exclude(**exclude_kwargs)
        return qs.count()
