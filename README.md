# What's that Lingo 🗣️

A semantic search engine for Urban Dictionary entries that helps you discover slang terms and their meanings using vector embeddings.

## What it does

This project allows you to search for slang terms using natural language queries and semantic similarity rather than exact keyword matching. For example:

Query: "What are some words originating from Toronto?"
Get relevant Urban Dictionary entries unlike Urban Dictionary search which will just give you the word "Toronto". 

It uses:
- **Vector Database**: Qdrant for storing and searching embeddings. I tried Weaviate but took too long to setup and get working, with bad embedding results so switched to Qdrant.
- **Embedding Model**: `nomic-embed-text-v1` for converting text to vectors
- **Data Source**: SQLite database containing Urban Dictionary entries
- **Search**: Semantic similarity search using cosine distance

## Usage

1. Scrape the Unofficial Urban Dictionary API and store results in SQLite using this schema:

```sql
CREATE TABLE meanings (
    meaning_id INTEGER PRIMARY KEY,
    word_id INTEGER,
    def_id TEXT,
    disambiguation TEXT,
    meaning TEXT NOT NULL,
    example TEXT,
    author TEXT,
    upvotes INTEGER,
    downvotes INTEGER,
    permalink TEXT,
    date_written DATE
);
```
save this as `urban_dictionary.db` in your project root. I did some post-processing with the data to try and eliminate words with bad scores or words that weren't relevant to not pollute it with bad embeddings.

2. Ingest the data into Qdrant or your vector database of choice using an valid embedding model. I used `nomic-embed-text-v1` but `v1.5` was something I want to try next time. 

I grouped the disambigation and meaning together when vectorizing but there are other ways for more meaningful embeddings like a hybrid/keyword search. 

3. Once vectorized, type in a query and see if your results are relevant and valuable. 

## Example Output

```python
query = "words originated from Toronto"
```

gives results like:

```
Query: words originated from Toronto?
Score: 0.85
Word ID: 1234
Word: Ahlie
Meaning: Tdot/Toronto slang for "right?"
Example: You're reaching my crib tonight ahlie?
--------------------
Query: words originated from Toronto?
Score: 0.82
Word ID: 2345
Word: Are you dumb or are you dumb
Meaning: Toronto slang, you tell someone when they’re acting stupid, or tryna be something they’re not. Pretty casually used, not that serious.
Example: are u dumb? You know who mans is? I’m not afraid of no wasteman!
--------------------
Query: words originated from Toronto?
Score: 0.82
Word ID: 3456
Word: nyeah eh
Meaning: A word the Toronto mandem use instead of OH REALLY usually used to confront someone or start a argument.
Example: Sayin He got that new LV belt from his dukes”
“nyeah eh sayin I’m bout to stain the man
--------------------
```