from django.contrib import admin

# Register your models here.

from .models import Roger_preprep_line, Todo_obj, Todo_phase

admin.site.register(Roger_preprep_line)
admin.site.register(Todo_obj)
admin.site.register(Todo_phase)
