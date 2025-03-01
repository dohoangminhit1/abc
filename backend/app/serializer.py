def convert_doc(document) -> dict:
    return{
        "_id": str(document["_id"]),
        "name": document["name"],
        "age": document["age"],
        "que": document["que"]
    }
    
def convert_doc_list(documents) -> list:
    return [convert_doc(document) for document in documents]