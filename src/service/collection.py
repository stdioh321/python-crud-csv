import os
from dotenv import load_dotenv
from src.repository.mongo_repository import MongoRepository
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')

collection_service = MongoRepository(MONGO_URI)
