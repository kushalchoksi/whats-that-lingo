So we have the docker compose which we use to spin up the docker containers

In these docker containers we have the weaviate database, the ollama model, and some other stuff 

- qna-transformers (nlp querying model)
- weaviate 1.26.1 (database)
- ollama (where the nomic model is being held in)
- reranker-transformers (re-ranking results)

CONTAINER ID   IMAGE                  COMMAND                  CREATED          STATUS          PORTS                                              NAMES
158925b464b3   weaviate:1.26.1        "/bin/weaviate --hos…"   21 seconds ago   Up 21 seconds   0.0.0.0:8080->8080/tcp, 0.0.0.0:50051->50051/tcp   weaviate-weaviate-1
4676667f011a   qna-transformers       "/bin/sh -c 'uvicorn…"   21 seconds ago   Up 21 seconds                                                      weaviate-qna-1
ed2cb4d04d48   reranker               "/bin/sh -c 'uvicorn…"   21 seconds ago   Up 21 seconds                                                      weaviate-reranker-1
baf68cdaa59c   ollama/ollama          "/bin/ollama serve"      21 seconds ago   Up 21 seconds   11434/tcp                                          weaviate-ollama-1

What we want to try is embed the test database

1) Read from sqlite database
2) Fetch data from tables

3) Use Ollama to generate embeddings

4) Insert the embeddings into Weaviate

-----------------

Saturday, October 5th, '24

Created vectorizer.py - creates the weaviate schema
Created check_vectorizer.py - which checks if the vectorizer was schema was created
Created data-import.py - which will embed the shits into weaviate according to the schema

-----------------

0|meaning_id|INTEGER|0||1
1|word_id|INTEGER|0||0
2|def_id|TEXT|0||0
3|disambiguation|TEXT|0||0
4|meaning|TEXT|1||0
5|example|TEXT|0||0
6|author|TEXT|0||0
7|upvotes|INTEGER|0||0
8|downvotes|INTEGER|0||0
9|permalink|TEXT|0||0
10|date_written|DATE|0||0

----------------

