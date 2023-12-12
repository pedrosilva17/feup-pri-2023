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

        docs = []

        fr = requests.get("http://meic_solr:8983/solr/causes/query?q=*:*&q.op=OR&rows=100&defType=edismax&indent=true&wt=json&start=0&useParams=").json()
        numFound = fr.get('response').get('numFound')
        docs.extend(fr.get('response').get('docs'))

        for i in range(100, numFound, 100):
            fr = requests.get("http://meic_solr:8983/solr/causes/query?q=*:*&q.op=OR&rows=100&defType=edismax&indent=true&wt=json&start=" + str(i) + "&useParams=").json()
            docs.extend(fr.get('response').get('docs'))

        countries = {}

        for doc in docs:
            print(doc.get("cca3"))
            print(doc.get("location_name"))
            cca3 = doc.get("cca3")[0]
            val = doc.get("val")
            cause_name = doc.get("cause_name")

            if cca3 not in countries:
                countries[cca3] = {}

            if cause_name not in countries[cca3]:
                countries[cca3][cause_name] = 0

            countries[cca3][cause_name] += val

        print(countries)

        return Response(data)

class AdvancedSearch(APIView):
    
    def put(self, request):
        data = json.loads(request.body)
        return Response(data)