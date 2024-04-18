from rest_framework.serializers import ModelSerializer
from base_app.models import Roger_preprep_line

class Serializer_Roger_preprep_line(ModelSerializer):
    class Meta:
        model = Roger_preprep_line
        fields = '__all__'