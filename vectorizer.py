import weaviate
from weaviate.classes.config import Configure, Property, DataType

client = weaviate.connect_to_local()  # Connect with default parameters

try:
    print(client.is_connected)
    print(client.cluster.nodes)

    client.collections.delete("VectorMeanings")

    client.collections.create(
        "VectorMeanings",
        vectorizer_config=[
            # Set a named vector
            Configure.NamedVectors.text2vec_ollama(
                name="vector_meaning",
                source_properties=["vector_meaning"],
                api_endpoint="http://host.docker.internal:11434",  # If using Docker, use this to contact your local Ollama instance
                model="nomic-embed-text",  # The model to use, e.g. "nomic-embed-text"
            ),
        ],
        properties=[  # Define properties
            Property(name="vector_meaning", data_type=DataType.TEXT),
            Property(name="meaning_id", data_type=DataType.INT),
            Property(name="word_id", data_type=DataType.INT),
        ],
    )

finally:
    client.close()  # Ensure the connection is closed

