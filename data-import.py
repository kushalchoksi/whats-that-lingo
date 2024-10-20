import weaviate
import sqlite3
import re
from weaviate.classes.config import Configure, Property, DataType

# Connect to SQLite database
def connect_to_sqlite(db_path):
    return sqlite3.connect(db_path)

# Read data from SQLite
def read_from_sqlite(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    return rows, columns

# Connect to Weaviate
def connect_to_weaviate():
    return weaviate.connect_to_local()

# Create Weaviate collection
def get_weaviate_collection(client, collection_name, properties):
    return client.collections.get(collection_name)

# Insert data into Weaviate
def insert_into_weaviate(collection, data, columns):
    with collection.batch.dynamic() as batch:
        index = 0
        for row in data:
            index += 1
            obj = {col: val for col, val in zip(columns, row)}
            
            meaning = re.sub(r"\[(.*?)\]", r"\1", obj['meaning'])

            weaviate_obj = {
                "meaning_id": obj["meaning_id"],
                "word_id": obj["word_id"],
                "vector_meaning": meaning
            }

            # The model provider integration will automatically vectorize the object
            batch.add_object(
                properties=weaviate_obj,
                # vector=vector  # Optionally provide a pre-obtained vector
            )
            print(f"Completed {index} of {len(data)}")


# Main function
def main():
    # SQLite configuration
    sqlite_db_path = "urban-dictionary-test.db"
    table_name = "meanings"

    # Weaviate configuration
    weaviate_url = "http://localhost:8080"
    weaviate_collection_name = "VectorMeanings"

    # Connect to SQLite and read data
    sqlite_conn = connect_to_sqlite(sqlite_db_path)
    rows, columns = read_from_sqlite(sqlite_conn, table_name)

    # Connect to Weaviate
    weaviate_client = connect_to_weaviate()

    # Define properties for Weaviate collection
    properties = [
        ("meaning_id", DataType.INT),
        ("word_id", DataType.INT),
        ("meaning_with_example", DataType.TEXT),
    ]

    # Create Weaviate collection
    collection = get_weaviate_collection(weaviate_client, weaviate_collection_name, properties)

    # Insert data into Weaviate
    insert_into_weaviate(collection, rows, columns)

    print(f"Inserted {len(rows)} rows into Weaviate collection '{weaviate_collection_name}'")

    # Close SQLite connection
    sqlite_conn.close()
    weaviate_client.close()

if __name__ == "__main__":
    main()

# client = weaviate.connect_to_local()

# try:
#     collection = client.collections.get("VectorMeanings")

#     with collection.batch.dynamic() as batch:
#         for src_obj in source_objects:
#             weaviate_obj = {
#                 "title": src_obj["title"],
#                 "description": src_obj["description"],
#             }

#             # The model provider integration will automatically vectorize the object
#             batch.add_object(
#                 properties=weaviate_obj,
#                 # vector=vector  # Optionally provide a pre-obtained vector
#             )

# finally:
#     client.close()

