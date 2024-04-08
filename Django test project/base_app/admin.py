from django.contrib import admin

# Register your models here.

from .models import Roger_preprep_line, Todo_obj, Todo_phase, Post_op, Post_reply, Wf_city

admin.site.register(Roger_preprep_line)
admin.site.register(Todo_obj)
admin.site.register(Todo_phase)
admin.site.register(Post_op)
admin.site.register(Post_reply)
admin.site.register(Wf_city)

# User list (for development/testing only, obviously shouldn't be just kept here like this)
# Admin_test / Test admin password
# Admin / aDmin1
# User_1 / Password_1
# User_2 / Password_2