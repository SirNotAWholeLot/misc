from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from base_app.models import Roger_preprep_line
from .serializers import Serializer_Roger_preprep_line, Serializer_Roger_line_name

@api_view(['GET']) # List of methods that are allowed for this view
def get_routes(request, format=None):
    routes = [
        'GET /api',
        'GET /api/roger_man/names/',
        'GET /api/roger_man',
        'GET /api/roger_man/item_id=:id',
        'POST /api/roger_man/item_id=:id',
        'DELETE /api/roger_man/item_id=:id',
    ]
    return Response(routes) # To get normal JSON, add /?format=json
    # JsonResponse(routes, safe=False) # Safe blocks converting vars other than Python dictionaries to JSON

# Basic API for the Roger Man
@api_view(['GET'])
def get_roger_line_names(request, format=None): # List of all lines - only IDs and names
    lines = Roger_preprep_line.objects.all()
    serializer = Serializer_Roger_line_name(lines, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_roger_lines(request, format=None): # Get all
    lines = Roger_preprep_line.objects.all()
    serializer = Serializer_Roger_preprep_line(lines, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST', 'DELETE'])
def get_roger_response(request, pk, format=None): # Get/put/delete a specific line
    if request.method == 'GET':
        try:
            response = Roger_preprep_line.objects.get(id=pk)
        except Roger_preprep_line.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = Serializer_Roger_preprep_line(response, many=False)
        return Response(serializer.data)
    elif request.method == 'POST': # Not sure how this interacts with the pk - POST requests aren't tested yet
        serializer = Serializer_Roger_preprep_line(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        try:
            item = Roger_preprep_line.objects.get(id=pk)
        except Roger_preprep_line.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
