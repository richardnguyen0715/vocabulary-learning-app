from pymongo import MongoClient
from bson.objectid import ObjectId

class FlashcardManager:
    def __init__(self, db_uri, db_name):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.collection = self.db['flashcards']

    def create_flashcard(self, term, definition):
        flashcard = {
            'term': term,
            'definition': definition
        }
        result = self.collection.insert_one(flashcard)
        return str(result.inserted_id)

    def get_flashcard(self, flashcard_id):
        return self.collection.find_one({'_id': ObjectId(flashcard_id)})

    def update_flashcard(self, flashcard_id, term, definition):
        self.collection.update_one(
            {'_id': ObjectId(flashcard_id)},
            {'$set': {'term': term, 'definition': definition}}
        )

    def delete_flashcard(self, flashcard_id):
        self.collection.delete_one({'_id': ObjectId(flashcard_id)})

    def get_all_flashcards(self):
        return list(self.collection.find())