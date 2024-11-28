import numpy as np
import math
import json
from preprocess import text_preprocessing


def vectorize_query(query, term2id, idf):
    tokens = text_preprocessing(query).split()
    # print(f'preprocessed query: {tokens}')
    tf = np.zeros(len(term2id))
    qvec = np.zeros(len(term2id))
    for token in tokens:
        if token not in term2id:
            continue
        id = term2id[token]
        cnt = tokens.count(token)
        tf[id] = (1 + math.log10(cnt)) if cnt > 0 else 0
    qvec = tf * idf
    norm = np.linalg.norm(qvec)
    if norm != 0:
        qvec /= norm
    return qvec


def cosine_similarity(qvec, dvec):
    return np.dot(qvec, dvec)

def retrieve_documents(query, tfidf, idf, term2id, doc2id, documents):
    retrieved_docs = []
    qvec = vectorize_query(query, term2id, idf)
    for title in documents.keys():
        did = doc2id[title]
        dvec = tfidf[:, did]
        sim = cosine_similarity(qvec, dvec)
        retrieved_docs.append((sim, did))
    retrieved_docs.sort(reverse=True)
    return retrieved_docs


def search_query(query, tfidf, idf, term2id, doc2id, id2doc, documents, top_k=None):
    retrieved_docs = retrieve_documents(query, tfidf, idf, term2id, doc2id, documents)
    results = []
    for sim, did in retrieved_docs[:top_k]:
        title = id2doc[did]
        content_snippet = ' '.join(documents[title].split()[:50])  # Get the first 50 words
        results.append({
            'title': title,
            'snippet': content_snippet,
            'similarity': sim
        })
    return results

def main():
    term2id, doc2id, id2doc, documents = get_dicts()
    tf, idf, tfidf = compute_tfidf(term2id, doc2id, documents)
    query_1 = "Đại Nội Huế"
    search_query(query_1, tfidf, idf, term2id, doc2id, id2doc, documents, top_k=3)

if __name__ == "__main__":
    main()