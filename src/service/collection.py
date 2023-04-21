import os
from dotenv import load_dotenv
from src.repository.mongo_repository import MongoRepository
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')


class CollectionService:
    repo = MongoRepository(MONGO_URI)

    @staticmethod
    def create_collection(name, data):
        return CollectionService.repo.create_collection(data)

    @staticmethod
    def find_by_id(collection_name, id):
        return CollectionService.repo.find_by_id(collection_name, id)

    @staticmethod
    def find(collection_name: str, query: dict):
        return CollectionService.repo.find(collection_name, query)

    @staticmethod
    def insert(collection_name: str, document: dict):
        return CollectionService.repo.insert(collection_name, document)

    @staticmethod
    def update_patch(collection_name, query, data):
        return CollectionService.repo.update_patch(collection_name, query, data)

    @staticmethod
    def update_put(collection_name, query, data):
        return CollectionService.repo.update_put(collection_name, query, data)

    @staticmethod
    def delete(collection_name, query):
        return CollectionService.repo.delete(collection_name, query)
