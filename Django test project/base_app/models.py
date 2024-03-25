from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Roger_preprep_line(models.Model): # Lines for the Roger Man
    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=80)
    line = models.TextField(max_length=200)
    note = models.TextField(null=False, blank=True, max_length = 100)

    def __str__(self):
        return self.name
    
class Todo_obj(models.Model): # Major objectives for the to-do list. Each can have multiple phases
    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)    # For some reason, I can't make the timestamps work yet
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def short_desc(self):   # Short description as a function because unfortunately I can't just put this code into a template directly
        return self.description if len(self.description) <= 50 else (self.description[0:46] + '...')
    
#    def save(self, *args, **kwargs):
#        # On save, manually update timestamps
#        if not self.id:
#            self.created = timezone.now()
#        self.modified = timezone.now()
#        return super(Todo_obj, self).save(*args, **kwargs)    

class Todo_phase(models.Model): # Phases are essentially sub-objectives for the to-do list, they have a similar structure
    id = models.AutoField(primary_key=True) 
    objective = models.ForeignKey(Todo_obj, on_delete=models.CASCADE) # Removing objective -> remove all it's phases
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def short_desc(self):
        return self.description if len(self.description) <= 50 else (self.description[0:46] + '...')
    
class Post_op(models.Model): # Opening post
    id = models.AutoField(primary_key=True)
    poster = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True) # Should refer to the last reply time
    created = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True) # I couldn't find a good way to make use of ManyToManyField

    class Meta:
        ordering = ['-updated', '-created'] # The '-' before the field inverts sorting order

    def __str__(self):
        return self.title
    
    def short_body(self):
        return self.body if len(self.body) <= 50 else (self.body[0:46] + '...')

    def num_replies(self):
        return Post_reply.objects.filter(original=self.id).count()

class Post_reply(models.Model): # Reply: tied to an opening post
    id = models.AutoField(primary_key=True)
    poster = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    original = models.ForeignKey(Post_op, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    #updated = models.DateTimeField(auto_now=True) # Editing functionality is not supported yet
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.short_body()
    
    def short_body(self):
        return self.body if len(self.body) <= 50 else (self.body[0:46] + '...')
