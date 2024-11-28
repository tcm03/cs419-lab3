# Boolean and Vector Space Retrieval Models

This project implements two information retrieval models in Python: the Boolean Retrieval Model and the Vector Space Model. Each model is implemented in a separate script (`bool_retrieval.py` and `vector_space.py`), and this README file documents the primary functions and their usage in each script.

---

## Table of Contents
- [Boolean Retrieval Model](#boolean-retrieval-model)
  - [Functions](#boolean-retrieval-functions)
  - [Usage](#boolean-retrieval-usage)
- [Vector Space Model](#vector-space-model)
  - [Functions](#vector-space-functions)
  - [Usage](#vector-space-usage)

---

## Boolean Retrieval Model

The Boolean Retrieval Model uses boolean operators (`AND`, `OR`, `NOT`) to match documents containing specific terms. 

### Boolean Retrieval Functions

#### `get_docs()`
- Returns a dictionary of predefined documents, along with mappings between document titles and IDs.
- Output:
  - `documents`: dictionary containing document titles as keys and content as values.
  - `doc_id`: dictionary mapping document titles to unique IDs.
  - `inv_doc_id`: dictionary mapping document IDs to titles.

#### `build_index(documents, doc_id)`
- Constructs an inverted index mapping terms to the list of document IDs where they appear.
- Input:
  - `documents`: dictionary of documents.
  - `doc_id`: dictionary of document IDs.
- Output:
  - `index`: dictionary where each term is associated with a sorted list of document IDs.

#### `split(string, tokens)`
- Splits a query string into operands (terms) and operators (`AND`, `OR`).
- Input:
  - `string`: query string.
  - `tokens`: list of operators (`AND`, `OR`).
- Output:
  - `operands`: list of query terms.
  - `operators`: list of operators in the query.

#### `merge_postings(postings1, postings2, operator)`
- Merges two posting lists based on the boolean operator (`AND`, `OR`).
- Input:
  - `postings1`: list of document IDs for the first operand.
  - `postings2`: list of document IDs for the second operand.
  - `operator`: string, either `AND` or `OR`.
- Output:
  - A merged list of document IDs.

#### `get_posting(operand, index, doc_id)`
- Retrieves the posting list of documents for a given operand, handling `NOT` operators.
- Input:
  - `operand`: the term or `NOT` term to search.
  - `index`: inverted index.
  - `doc_id`: document IDs.
- Output:
  - A list of document IDs matching the operand condition.

#### `process_query(query, doc_id, index)`
- Processes a boolean query and returns a list of document IDs that match.
- Input:
  - `query`: query string with boolean operators.
  - `doc_id`: document IDs.
  - `index`: inverted index.
- Output:
  - List of matching document IDs.

#### `search_query(query, documents, doc_id, inv_doc_id, index)`
- Performs a query search and prints matching documents.
- Input:
  - `query`: query string.
  - `documents`: dictionary of document contents.
  - `doc_id`, `inv_doc_id`: mappings between document titles and IDs.
  - `index`: inverted index.

### Boolean Retrieval Usage
To use the Boolean Retrieval Model:
1. Run `bool_retrieval.py`.
2. Example queries:
   - `"Brutus AND Caesar AND NOT Calpurnia"`
   - `"mercy OR Caesar"`
   - `"NOT Caesar"`
   - `"Antony AND NOT mercy"`
   
---

## Vector Space Model

The Vector Space Model ranks documents based on cosine similarity to a query. It uses term frequency-inverse document frequency (TF-IDF) for document and query vectorization.

### Vector Space Functions

#### `get_dicts()`
- Returns documents in lowercase, along with mappings for document and term IDs.
- Output:
  - `term2id`: dictionary mapping each term to a unique ID.
  - `doc2id`: dictionary mapping each document title to a unique ID.
  - `id2doc`: dictionary mapping each document ID to a title.
  - `documents`: dictionary with document titles as keys and content as values.

#### `compute_tfidf(term2id, doc2id, documents)`
- Computes TF, IDF, and TF-IDF values for terms across documents.
- Input:
  - `term2id`: term IDs.
  - `doc2id`: document IDs.
  - `documents`: document contents.
- Output:
  - `tf`: term frequency matrix.
  - `idf`: inverse document frequency array.
  - `tfidf`: normalized TF-IDF matrix for documents.

#### `vectorize_query(query, term2id, idf)`
- Converts a query into a TF-IDF vector.
- Input:
  - `query`: query string.
  - `term2id`: term IDs.
  - `idf`: inverse document frequency array.
- Output:
  - Normalized TF-IDF vector for the query.

#### `cosine_similarity(qvec, dvec)`
- Calculates cosine similarity between the query vector and a document vector.
- Input:
  - `qvec`: query vector.
  - `dvec`: document vector.
- Output:
  - Cosine similarity score.

#### `retrieve_documents(query, tfidf, idf, term2id, doc2id, documents)`
- Ranks documents by cosine similarity to the query.
- Input:
  - `query`: query string.
  - `tfidf`: TF-IDF matrix for documents.
  - `idf`: inverse document frequency array.
  - `term2id`, `doc2id`: mappings for terms and documents.
  - `documents`: document contents.
- Output:
  - List of documents and their similarity scores.

#### `search_query(query, tfidf, idf, term2id, doc2id, id2doc, documents, top_k=None)`
- Searches for documents most similar to the query and prints results.
- Input:
  - `query`: query string.
  - `tfidf`, `idf`: TF-IDF matrix and IDF array.
  - `term2id`, `doc2id`, `id2doc`: term and document mappings.
  - `documents`: document contents.
  - `top_k`: (optional) number of top results to display.

### Vector Space Usage
To use the Vector Space Model:
1. Run `vector_space.py`.
2. Example queries:
   - `"Antony Cleopatra"`
   - `"Brutus Caesar"`
   - `"mercy worser"`

---

