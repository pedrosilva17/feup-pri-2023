import json

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class Search(APIView):
    
    def put(self, request):
        data = json.loads(request.body)
        return Response(data)

class AdvancedSearch(APIView):
    
    def put(self, request):
        data = json.loads(request.body)
        return Response(data)