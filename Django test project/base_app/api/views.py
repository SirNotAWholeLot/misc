from rest_framework.decorators import api_view
from rest_framework.response import Response
from base_app.models import Roger_preprep_line
from .serializers import Serializer_Roger_preprep_line

@api_view(['GET']) # List of methods that are allowed for this view
def get_routes(request):
    routes = [
        'GET /api',
        'GET /api/roger_man',
        'GET /api/roger_man/item_id=:id'
    ]
    return Response(routes) # To get normal JSON, add /?format=json
    # JsonResponse(routes, safe=False) # Safe blocks converting vars other than Python dictionaries to JSON

# Basic API for the Roger Man
@api_view(['GET'])
def get_roger_lines(request):
    lines = Roger_preprep_line.objects.all()
    serializer = Serializer_Roger_preprep_line(lines, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_roger_response(request, pk):
    response = Roger_preprep_line.objects.get(id=pk)
    serializer = Serializer_Roger_preprep_line(response, many=False)
    return Response(serializer.data)