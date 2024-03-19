from django.forms import ModelForm
from .models import Roger_preprep_line

class Form_Roger_preprep_line(ModelForm):
    class Meta:
        model = Roger_preprep_line
        fields = ['name', 'line', 'note'] # '__all__'