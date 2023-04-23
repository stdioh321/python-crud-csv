import uuid
from bson import ObjectId
from pymongo import MongoClient, InsertOne, errors
from datetime import datetime


class MongoRepository:
    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.db = self.client.get_database()

    def list_collections(self):
        return self.db.list_collection_names()

    def collection_exists(self, collection_name):
        return collection_name in self.db.list_collection_names()

    def create_collection(self, name=None):
        if name is None:
            name = str(uuid.uuid4())
        if self.collection_exists(name):
            raise errors.DuplicateKeyError("Collection already exists")
        self.db.create_collection(name)
        return name

    def create_collection_with_data(self, data):
        collection_name = str(uuid.uuid4())
        self.db[collection_name].insert_many(data)
        return collection_name

    def find_by_id(self, collection_name, id):
        doc = self.db[collection_name].find_one({"_id": ObjectId(id)})
        return self.format_document(doc) if doc else None

    def find(self, collection_name: str, query: dict):
        db = self.client.get_database()
        collection = db[collection_name]
        self.id_to_object_id(query)
        results = collection.find(query)
        return [self.format_document(result) for result in results]

    def insert(self, collection_name: str, document: dict):
        collection = self.db[collection_name]
        timestamp = datetime.utcnow()
        document['createdAt'] = timestamp
        document['updatedAt'] = timestamp
        result = collection.insert_one(document)
        return self.format_document(self.find_by_id(collection_name, result.inserted_id))

    def insert_many(self, collection_name: str, documents: list):
        collection = self.db[collection_name]
        timestamp = datetime.utcnow()

        for document in documents:
            document.setdefault('createdAt', timestamp)
            document.setdefault('updatedAt', timestamp)

        result = collection.insert_many(documents)
        return len(result.inserted_ids)

    def update_patch(self, collection_name, query, data):
        collection = self.db[collection_name]
        self.id_to_object_id(query)
        result = collection.update_many(query, {"$set": data})
        return result.matched_count

    def update_put(self, collection_name, query, data):
        collection = self.db[collection_name]
        self.id_to_object_id(query)
        result = collection.update_many(query, data)
        return result.matched_count

    def delete(self, collection_name, query):
        collection = self.db[collection_name]
        self.id_to_object_id(query)
        result = collection.delete_many(query)
        return result.deleted_count

    def id_to_object_id(self, query):
        if '_id' in query:
            query['_id'] = ObjectId(query['_id'])

    def format_document(self, doc: dict):
        if not doc:
            return None
        formatted_doc = {}
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                formatted_doc[key] = str(value)
            elif isinstance(value, datetime):
                formatted_doc[key] = int(value.timestamp())
            elif isinstance(value, list):
                formatted_doc[key] = [self.format_document(
                    item) if isinstance(item, dict) else item for item in value]
            elif isinstance(value, dict):
                formatted_doc[key] = self.format_document(value)
            else:
                formatted_doc[key] = value
        return formatted_doc
