import sys
import json
from sentence_transformers import SentenceTransformer

# Load the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    # The model.encode() method already returns a list of floats
    return model.encode(text, convert_to_tensor=False).tolist()

if __name__ == "__main__":
    # Read JSON from STDIN
    f = open('./datasets/generated/sample.json')
    data = json.load(f)

    # Update each document in the JSON data
    for document in data:
        # Extract fields if they exist, otherwise default to empty strings
        cause = document.get("cause_name", "")
        description = document.get("description", "")
        location = document.get("location_name", "")
        sex = document.get("sex_name", "")

        combined_text = f"{cause} {description} {location} {sex}"
        document["vector"] = get_embedding(combined_text)

    # Output updated JSON to STDOUT
    json.dump(data, sys.stdout, indent=4, ensure_ascii=False)
