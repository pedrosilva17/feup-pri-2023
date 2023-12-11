import json
import requests

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.


"""
{'sex': 'male', 'age': '20-54', 'min_year': 11, 'max_year': 12, 'min_value': 1, 'search_for': ['country', 'value', 'description', 'disease']}

"""

class Search(APIView):
    
    def put(self, request):
        data = json.loads(request.body)
        print(data)
        

        if (data.get('search_for') != None):
            pass

        if (data.get('search_for') != []):
            pass
        else:
            pass

        if (data.get('sex') != None):
            pass
        
        if (data.get('age') != None):
            pass

        if (data.get('min_year') != None):
            pass

        if (data.get('max_year') != None):
            pass

        if (data.get('min_value') != None):
            pass

        if (data.get('max_value') != None):
            pass

        if (data.get('country') != None):
            pass


        return Response(requests.get("http://meic_solr:8983/solr/causes/query?q=*:*&q.op=OR&indent=true&useParams=").json())

        return Response(data)

class AdvancedSearch(APIView):
    
    def put(self, request):
        data = json.loads(request.body)
        return Response(data)