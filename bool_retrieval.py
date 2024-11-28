# Full name: Tu Canh Minh
# SID: 21125019
# Class: 21CTT

### TASK 1: BOOLEAN RETRIEVAL

supported_operands = ['AND', 'OR']

def get_docs():
    documents = {
        "Antony and Cleopatra": "Antony Brutus Caesar Cleopatra mercy worser",
        "Julius Caesar": "Antony Brutus Caesar Calpurnia",
        "The tempest": "mercy worser",
        "Hamlet": "Brutus Caesar mercy worser",
        "Othello": "Caesar mercy worser",
        "Macbeth": "Antony Caesar mercy"
    }
    doc_id = {}
    inv_doc_id = {}
    for title in documents.keys():
        id = len(doc_id)
        doc_id[title] = id
        inv_doc_id[id] = title
    return documents, doc_id, inv_doc_id

def build_index(documents, doc_id):
    index = {}
    for title, content in documents.items():
        for word in content.split():
            if word not in index:
                index[word] = []
            index[word].append(doc_id[title])
    # sort index based on doc frequency
    index = {k: v for k, v in sorted(index.items(), key=lambda item: len(item[1]))}
    # sort each posting list
    for word in index.keys():
        index[word] = sorted(list(set(index[word])))
    return index

def split(string, tokens):
    idx = 0
    operands = []
    operators = []
    for i in range(len(string)):
        for tok in tokens:
            if i+len(tok) <= len(string) and string[i:i+len(tok)] == tok:
                operands.append(string[idx:i].strip())
                operators.append(tok)
                idx = i+len(tok)
    if string[idx:].strip() != "":
        operands.append(string[idx:].strip())
    return operands, operators

def merge_postings(postings1, postings2, operator):

    if operator == 'AND':
        i = 0
        j = 0
        result = []
        while i < len(postings1) and j < len(postings2):
            if postings1[i] == postings2[j]:
                result.append(postings1[i])
                i += 1
                j += 1
            elif postings1[i] < postings2[j]:
                i += 1
            else:
                j += 1
        return result
    
    elif operator == 'OR':
        i = 0
        j = 0
        result = []
        while i < len(postings1) and j < len(postings2):
            if postings1[i] == postings2[j]:
                result.append(postings1[i])
                i += 1
                j += 1
            elif postings1[i] < postings2[j]:
                result.append(postings1[i])
                i += 1
            else:
                result.append(postings2[j])
                j += 1
        while i < len(postings1):
            result.append(postings1[i])
            i += 1
        while j < len(postings2):
            result.append(postings2[j])
            j += 1
        return result
    
    else:
        raise ValueError("Invalid operator")
    
def get_posting(operand, index, doc_id):
    complement = False
    if len(operand) > 3 and operand.lstrip()[:3] == 'NOT':
        complement = True
        operand = operand.lstrip()[3:].strip()
    if operand not in index:
        return []
    elif complement:
        return list(sorted(set(doc_id.values()) - set(index[operand])))
    else:
        return index[operand]

def process_query(query, doc_id, index):
    """
    Examples:
    "Brutus AND Caesar AND NOT Calpurnia"
    "mercy OR Caesar"
    """

    operands, operators = split(query, ["AND", "OR"])
    prev_posting = get_posting(operands[0], index, doc_id)
    for i, operator in enumerate(operators):
        next_opr = operands[i+1]
        next_posting = get_posting(next_opr, index, doc_id)
        prev_posting = merge_postings(prev_posting, next_posting, operator)
    return prev_posting

def search_query(query, documents, doc_id, inv_doc_id, index):
    print('QUERY:', query)
    doc_ids = process_query(query, doc_id, index)
    found_docs = []
    print('FOUND DOCUMENTS:\n')
    for did in doc_ids:
        title = inv_doc_id[did]
        print(title)
        print(documents[title])
        print()

def main():
    documents, doc_id, inv_doc_id = get_docs()
    index = build_index(documents, doc_id)
    query_1 = "Brutus AND Caesar AND NOT Calpurnia"
    search_query(query_1, documents, doc_id, inv_doc_id, index)
    query_2 = "mercy OR Caesar"
    search_query(query_2, documents, doc_id, inv_doc_id, index)
    query_3 = "NOT Caesar"
    search_query(query_3, documents, doc_id, inv_doc_id, index)
    query_4 = "Antony AND NOT mercy"
    search_query(query_4, documents, doc_id, inv_doc_id, index)

if __name__ == "__main__":
    main()