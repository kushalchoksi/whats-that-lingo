import weaviate
import json

client = weaviate.connect_to_local()

try:
    collection = client.collections.get('VectorMeanings')

    response = collection.query.near_text(
        query="girl",  # The model provider integration will automatically vectorize the query
        limit=20
    )

    print(response.objects)

    for obj in response.objects:
        print(obj.properties["vector_meaning"])

finally:
    client.close()