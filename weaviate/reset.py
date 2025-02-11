import weaviate
from weaviate.classes.query import Filter

client = weaviate.connect_to_local()

collection = client.collections.get("VectorMeanings")


try:
    response = collection.aggregate.over_all(
        total_count=True
    )

    print(response.total_count)


finally:
    client.close()
