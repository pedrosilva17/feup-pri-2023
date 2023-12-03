from django.shortcuts import render

# Create your views here.

class Search:
    
    def list(self, request):
        data = request.query_params;
        return Response(data)

class AdvancedSearch:
    
    def list(self, request):
        data = request.query_params;
        return Response(data)