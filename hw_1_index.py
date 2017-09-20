def create_index(docs):
    final_index = {}
    for d in range(len(docs)):
        for term in docs[d]:
            if term not in final_index:
                final_index[term] = [d]
            else:
                final_index[term].append(d)
    return final_index
