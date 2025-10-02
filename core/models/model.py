import uuid
from django.db import models
from django.conf import settings


# Create your models here.


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    inactive = models.BooleanField(default=False, null=True, blank=False)
    deleted = models.BooleanField(default=False, null=True, blank=False)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, db_index=True, editable=False,
                                   on_delete=models.SET_NULL, related_name="%(class)s_created")
    updated_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, db_index=True, editable=False,
                                   on_delete=models.SET_NULL, related_name="%(class)s_updated")

    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, db_index=True, editable=False,
                                   on_delete=models.SET_NULL, related_name="%(class)s_deleted")

    class Meta:
        abstract = True
