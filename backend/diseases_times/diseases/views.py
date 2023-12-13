import json
import requests
from sentence_transformers import SentenceTransformer

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class Search(APIView):
    
    def put(self, request):
        def boost(field):
            match field:
                case "cause_name":
                    return "1.5"
                case "description":
                    return "2"
                # case "val":
                #     return "0.75"
                case "location_name":
                    return "1"
                case _:
                    return "1"

        data = json.loads(request.body)
        query = "http://meic_solr:8983/solr/causes/query?"
        q = ""

        if (data.get('search_for') != None):
            pass

        if (data.get('search_for') != []):
            fields = data.get('search_for')
            term = ""
            if (data.get('search') != None):
                terms = data.get('search')
            else:
                terms = "*"

            q += (" OR ".join([f'{field}:{terms}~^{boost(field)}' for field in fields]))
        else:
            fields = ["cause_name", "description", "val", "location_name"]
            term = ""
            if (data.get('search') != None):
                terms = data.get('search')
            else:
                terms = "*"

            q += (" OR ".join([f'{field}:{terms}~^{boost(field)}' for field in fields]))

        if (data.get('sex') != None):
            pass
        
        if (data.get('age') != None):
            age = ""
            match data.get('age'):
                case "0-19":
                    age = '"<20 years"'
                case "20-54":
                    age = '"20-54 years"'
                case "55-99":
                    age = '"55+ years"'
            q += " AND age:" + age

        if (data.get('min_year') != None and data.get('max_year') != None):
            q += " AND year:[" + str(data.get('min_year')) + " TO " + str(data.get('max_year')) + "]"
        elif (data.get('min_year') != None and data.get('max_year') == None):
            q += " AND year:[" + str(data.get('min_year')) + " TO *]"
        elif (data.get('max_year') == None and data.get('min_year') != None):
            q += " AND year:[* TO " + str(data.get('max_year')) + "]"


        if (data.get('min_value') != None and data.get('max_value') != None):
            q += " AND val:[" + str(data.get('min_value')) + " TO " + str(data.get('max_value')) + "]"
        elif (data.get('min_value') != None and data.get('max_value') == None):
            q += " AND val:[" + str(data.get('min_value')) + " TO *]"
        elif (data.get('min_value') == None and data.get('max_value') != None):
            q += " AND val:[* TO " + str(data.get('max_value')) + "]"

        if (data.get('country') != None):
            q += " AND cca3:" + data.get('country')

        print("executing query:", f'{query}q={q}&rows=100&defType=edismax&indent=true&wt=json&start=0&useParams=')

        docs = []
        fr = requests.get(f'{query}q={q}&rows=100&defType=edismax&indent=true&wt=json&start=0&useParams=').json()
        numFound = fr.get('response').get('numFound')
        docs.extend(fr.get('response').get('docs'))

        for i in range(100, numFound, 100):
            fr = requests.get(f'{query}q={q}&rows=100&defType=edismax&indent=true&wt=json&start={str(i)}&useParams=').json()

            docs.extend(fr.get('response').get('docs'))

        countries = {}

        for doc in docs:
            cca3 = doc.get("cca3")[0]
            val = doc.get("val")
            cause_name = doc.get("cause_name")

            if cca3 not in countries:
                countries[cca3] = {}

            if cause_name not in countries[cca3]:
                countries[cca3][cause_name] = 0

            countries[cca3][cause_name] += val
        
        for country in countries:
            tot = 0
            for cause in countries[country]:
                tot += countries[country][cause]

            countries[country]["median"] = tot / len(countries[country])

        max_value = float('-inf')
        min_value = float('inf')

        for country in countries:
            if countries[country]["median"] > max_value:
                max_value = countries[country]["median"]
            if countries[country]["median"] < min_value:
                min_value = countries[country]["median"]

        response = {
            "countries": countries,
            "max_value": max_value,
            "min_value": min_value,
            "docs": docs
        }
        return Response(response)

class AdvancedSearch(APIView):
    
    def text_to_embedding(self, query):
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embedding = model.encode(query, convert_to_tensor=False).tolist()

        embedding_str = f"[{','.join(map(str, embedding))}]"
        return embedding_str

    def put(self, request):
        def boost(field):
            match field:
                case "cause_name":
                    return "1.5"
                case "description":
                    return "2"
                # case "val":
                #     return "0.75"
                case "location_name":
                    return "1"
                case _:
                    return "1"

        data = json.loads(request.body)
        q = ""

        if (data.get('search_for') != None):
            pass

        if (data.get('search_for') != []):
            fields = data.get('search_for')
            term = ""
            if (data.get('search') != None):
                terms = data.get('search')
            else:
                terms = "*"

            q += (" OR ".join([f'{field}:{terms}~^{boost(field)}' for field in fields]))
        else:
            fields = ["cause_name", "description", "val", "location_name"]
            term = ""
            if (data.get('search') != None):
                terms = data.get('search')
            else:
                terms = "*"

            q += (" OR ".join([f'{field}:{terms}~^{boost(field)}' for field in fields]))

        if (data.get('sex') != None):
            pass
        
        if (data.get('age') != None):
            age = ""
            match data.get('age'):
                case "0-19":
                    age = '"<20 years"'
                case "20-54":
                    age = '"20-54 years"'
                case "55-99":
                    age = '"55+ years"'
            q += " AND age:" + age

        if (data.get('min_year') != None and data.get('max_year') != None):
            q += " AND year:[" + str(data.get('min_year')) + " TO " + str(data.get('max_year')) + "]"
        elif (data.get('min_year') != None and data.get('max_year') == None):
            q += " AND year:[" + str(data.get('min_year')) + " TO *]"
        elif (data.get('max_year') == None and data.get('min_year') != None):
            q += " AND year:[* TO " + str(data.get('max_year')) + "]"


        if (data.get('min_value') != None and data.get('max_value') != None):
            q += " AND val:[" + str(data.get('min_value')) + " TO " + str(data.get('max_value')) + "]"
        elif (data.get('min_value') != None and data.get('max_value') == None):
            q += " AND val:[" + str(data.get('min_value')) + " TO *]"
        elif (data.get('min_value') == None and data.get('max_value') != None):
            q += " AND val:[* TO " + str(data.get('max_value')) + "]"

        if (data.get('country') != None):
            q += " AND cca3:" + data.get('country')

        endpoint = "http://meic_solr:8983/solr"
        collection = "causes"

        embedding = self.text_to_embedding(q)
        
        url = f"{endpoint}/{collection}/select"
        docs = []
        
        start = 0
        while (True):

            data = {
                'q': f"{{!knn f=vector topK={start + 1000}}}{embedding}",
                'start': start,
                'rows': 1000,
                'wt': "json"
            }
        
            headers = { 'Content-Type': "application/x-www-form-urlencoded"}
            response = requests.post(url, data = data, headers = headers)
            response = response.json()

            docs.extend(response.get('response').get('docs'))

            if (len(response.get('response').get('docs')) < 1000):
                break
            else:
                start += 1000

        countries = {}

        for doc in docs:
            cca3 = doc.get("cca3")[0]
            val = doc.get("val")
            cause_name = doc.get("cause_name")

            if cca3 not in countries:
                countries[cca3] = {}

            if cause_name not in countries[cca3]:
                countries[cca3][cause_name] = 0

            countries[cca3][cause_name] += val
        
        for country in countries:
            tot = 0
            for cause in countries[country]:
                tot += countries[country][cause]

            countries[country]["median"] = tot / len(countries[country])

        max_value = float('-inf')
        min_value = float('inf')

        for country in countries:
            if countries[country]["median"] > max_value:
                max_value = countries[country]["median"]
            if countries[country]["median"] < min_value:
                min_value = countries[country]["median"]

        response = {
            "countries": countries,
            "max_value": max_value,
            "min_value": min_value,
            "docs": docs
        }

        return Response(response)
