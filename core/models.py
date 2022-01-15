from django.db import models

class TimeStampModel(models.Model):
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField('삭제일', null=True, default=None)
    is_deleted   = models.BooleanField(default=False, verbose_name="Is Deleted")

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        if self.is_deleted : return
        self.is_deleted=True
        self.deleted_at = now()
        self.save(update_fields=['deleted_at'])

    def erase(self,*args,**kwargs):
        """
        Actually delete from database.
        """
        super(SoftDeleteModel,self).delete(*args,**kwargs)

    def restore(self,*args,**kwargs):
        if not self.deleted: return
        self.is_deleted=False
        self.deleted_at = None
        self.save()
        self.save(update_fields=['deleted_at'])