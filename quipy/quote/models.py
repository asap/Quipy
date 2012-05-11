from django.db import models

# Create your models here.
class Quote(models.Model):
    text = models.TextField()
    source = models.TextField()

    class Meta:
        pass
    def __unicode__(self):
        return self.text