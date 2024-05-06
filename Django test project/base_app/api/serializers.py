from rest_framework.serializers import ModelSerializer
from base_app.models import Roger_preprep_line

# This one is used to return the whole content of the Roger Man entry, when you either want to fetch a specific record or the whole database
class Serializer_Roger_preprep_line(ModelSerializer):
    class Meta:
        model = Roger_preprep_line
        fields = '__all__'

# Returns only the ID and the name - used to get the list of entries without unnecessary info
class Serializer_Roger_line_name(ModelSerializer):
    class Meta:
        model = Roger_preprep_line
        fields = ['id', 'name']