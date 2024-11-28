import os
from preprocess import preprocess
from get_data import get_dicts, get_scores
from vector_space import search_query

def main():
    
    # if the preprocessed data is not available
    if not os.path.exists("documents.json"):
        preprocess()

    # get dictionaries and ranking scores
    term2id, doc2id, id2doc, documents = get_dicts()
    tf, idf, tfidf = get_scores(term2id, doc2id, documents)

    query_1 = "Đại Nội Huế"
    search_query(query_1, tfidf, idf, term2id, doc2id, id2doc, documents, top_k=3)


if __name__ == "__main__":
    main()