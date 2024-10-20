import weaviate
import json

client = weaviate.connect_to_local()

try:
    x = client.collections.get('VectorMeanings')
    print(x)
    # print(json.dumps(x, sort_keys=True, indent=4))
finally:
    client.close()