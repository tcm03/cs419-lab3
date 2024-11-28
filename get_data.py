import numpy as np
import json
import os
import math
from preprocess import preprocess

def compute_dicts(documents):
    doc2id = {} # from document title -> document ID
    id2doc = {} # and reverse
    for title in documents.keys():
        id = len(doc2id)
        doc2id[title] = id
        id2doc[id] = title
    term2id = {} # from a raw term -> term ID
    for content in documents.values():
        for word in content.split():
            if word not in term2id:
                id = len(term2id)
                term2id[word] = id
    return term2id, doc2id, id2doc


def compute_tfidf(term2id, doc2id, documents):
    df = np.zeros(len(term2id))
    idf = np.zeros(len(term2id))
    N = len(documents)
    for term, tid in term2id.items():
        for content in documents.values():
            if term in content:
                df[tid] += 1
        idf[tid] = math.log10(N/df[tid])
    tf = np.zeros((len(term2id), N))
    for term, tid in term2id.items():
        for doc, did in doc2id.items():
            cnt = documents[doc].count(term)
            tf[tid, did] = (1 + math.log10(cnt)) if cnt > 0 else 0
    tfidf = tf * idf[:, np.newaxis]
    # normalize each document vector (column) in tfidf
    for i in range(N):
        norm = np.linalg.norm(tfidf[:, i])
        if norm != 0:
            tfidf[:, i] /= norm
    return tf, idf, tfidf

def save_scores(tf, idf, tfidf):
    np.savez_compressed('scores.npz', tf=tf, idf=idf, tfidf=tfidf)

def load_scores(file_path):
    if not os.path.exists(file_path):
        # print(f"Error: The file '{file_path}' does not exist.")
        return None, None, None
    try:
        with np.load(file_path) as data:
            tf = data['tf']
            idf = data['idf']
            tfidf = data['tfidf']
        return tf, idf, tfidf
    except Exception as e:
        # print(f"Error loading NPZ file: {e}")
        return None, None, None

def save_dicts(term2id, doc2id, id2doc):
    combined_dict = {
        "term2id": term2id,
        "doc2id": doc2id,
        "id2doc": id2doc
    }
    with open('dict.json', 'w', encoding = 'utf-8') as f:
        json.dump(combined_dict, f, indent=4, ensure_ascii=False)

def load_dicts(file_path):
    if not os.path.exists(file_path):
        return None, None, None
    try:
        with open(file_path, 'r') as f:
            combined_dict = json.load(f)
        term2id = combined_dict["term2id"]
        doc2id = combined_dict["doc2id"]
        id2doc = {int(k): v for k, v in combined_dict["id2doc"].items()}
        return term2id, doc2id, id2doc
    except Exception as e:
        return None, None, None

def get_dicts():
    if not os.path.exists('documents.json'):
        preprocess()
    with open('documents.json', encoding = 'utf-8') as f:
        documents = json.load(f)
    term2id, doc2id, id2doc = load_dicts("dict.json")
    if term2id is None:
        term2id, doc2id, id2doc = compute_dicts(documents)
        save_dicts(term2id, doc2id, id2doc)
    return term2id, doc2id, id2doc, documents
    
def get_scores(term2id, doc2id, documents):
    tf, idf, tfidf = load_scores("scores.npz")
    if tf is None:
        tf, idf, tfidf = compute_tfidf(term2id, doc2id, documents)
        save_scores(tf, idf, tfidf)
    return tf, idf, tfidf