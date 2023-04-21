import os
from dotenv import load_dotenv
from src.repository.mongo_repository import MongoRepository
from src.exceptions.custom_exception import CustomException

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')


class CollectionService:
    repo = MongoRepository(MONGO_URI)

    @staticmethod
    def collection_exists(collection_name):
        return CollectionService.repo.collection_exists(collection_name)

    @staticmethod
    def create_collection(data):
        return CollectionService.repo.create_collection(data)

    @staticmethod
    def clear_and_insert_many(collection_name, documents: list):
        if not CollectionService.collection_exists(collection_name):
            raise CustomException('Collection not found', status_code=404)
        CollectionService.repo.delete(collection_name, {})
        return CollectionService.repo.insert_many(collection_name, documents)

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
