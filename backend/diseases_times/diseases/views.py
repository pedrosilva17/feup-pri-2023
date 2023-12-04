from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class Search(APIView):
    
    def get(self, request):
        data = request.query_params
        return Response(data)

class AdvancedSearch(APIView):
    
    def get(self, request):
        data = request.query_params;
        return Response(data)