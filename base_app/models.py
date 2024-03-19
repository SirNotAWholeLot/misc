from django.db import models
from django.utils import timezone

# Create your models here.

class Roger_preprep_line(models.Model):
    #id = 
    name = models.CharField(max_length=80)
    line = models.TextField(max_length=200)
    note = models.TextField(null=False, blank=True, max_length = 100)

    def __str__(self):
        return self.name
    
class Todo_obj(models.Model):
#    id = 
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def short_desc(self):
        return self.description if len(self.description) <= 50 else (self.description[0:46] + '...')
    
#    def save(self, *args, **kwargs):
#        # On save, manually update timestamps
#        if not self.id:
#            self.created = timezone.now()
#        self.modified = timezone.now()
#        return super(Todo_obj, self).save(*args, **kwargs)
    

class Todo_phase(models.Model):
    objective = models.ForeignKey(Todo_obj, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def short_desc(self):
        return self.description if len(self.description) <= 50 else (self.description[0:46] + '...')
