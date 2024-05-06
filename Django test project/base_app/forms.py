from django.forms import ModelForm
from .models import Roger_preprep_line, Post_op, Post_reply

class Form_Roger_preprep_line(ModelForm): # Very basic form for Roger Man's database
    class Meta:
        model = Roger_preprep_line
        fields = ['name', 'line', 'note'] # '__all__'

class Form_Post_op(ModelForm):
    class Meta:
        model = Post_op
        fields = ['title', 'body'] # All other fields are filled automatically

class Form_Post_reply(ModelForm):
    class Meta:
        model = Post_reply
        fields = ['body']