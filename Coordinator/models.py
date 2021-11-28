from django.db import models

# Create your models here.
def csv_path(instance):
    return os.path.join("csvs/{0}".format(instance.doc))


class Csv(models.Model):
    doc = models.FileField(upload_to="csv_path")
    
    def __str__(self):
        return self.doc

    def delete(self,using=None,keep_parents=False):
        self.doc.storage.delete(self.doc.name)
        super().delete()