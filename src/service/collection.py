import os
from dotenv import load_dotenv
from src.repository.mongo_repository import MongoRepository
from src.exceptions.custom_exception import CustomException

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')


class CollectionService:
    repo = MongoRepository(MONGO_URI)

    @staticmethod
    def list_collections():
        return CollectionService.repo.list_collections()

    @staticmethod
    def collection_exists(collection_name):
        return CollectionService.repo.collection_exists(collection_name)

    @staticmethod
    def create_collection(data):
        return CollectionService.repo.create_collection_with_data(data)

    @staticmethod
    def clear_and_insert_many(collection_name, documents: list):
        CollectionService.check_collection(collection_name)
        CollectionService.repo.delete(collection_name, {})
        return CollectionService.repo.insert_many(collection_name, documents)

    @staticmethod
    def find_by_id(collection_name, id):
        CollectionService.check_collection(collection_name)
        return CollectionService.repo.find_by_id(collection_name, id)

    @staticmethod
    def find(collection_name: str, query: dict):
        CollectionService.check_collection(collection_name)
        return CollectionService.repo.find(collection_name, query)

    @staticmethod
    def insert(collection_name: str, document: dict):
        CollectionService.check_collection(collection_name)
        return CollectionService.repo.insert(collection_name, document)

    @staticmethod
    def update_patch(collection_name, query, data):
        CollectionService.check_collection(collection_name)
        return CollectionService.repo.update_patch(collection_name, query, data)

    @staticmethod
    def update_put(collection_name, query, data):
        if len(data) < 1:
            raise CustomException('No data provided', status_code=400)

        CollectionService.check_collection(collection_name)
        return CollectionService.repo.update_put(collection_name, query, data)

    @staticmethod
    def delete(collection_name, query):
        CollectionService.check_collection(collection_name)
        return CollectionService.repo.delete(collection_name, query)

    @staticmethod
    def check_collection(collection_name: str):
        if not CollectionService.collection_exists(collection_name):
            raise CustomException(
                f'Collection \'{collection_name}\' not found', status_code=404)
