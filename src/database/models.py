from datetime import datetime
from bson import ObjectId

class VocabularyModel:
    def __init__(self, db):
        self.db = db
        self.collection = db.vocabulary
    
    def add_word(self, word_data):
        word_data['created_at'] = datetime.now()
        word_data['updated_at'] = datetime.now()
        return self.collection.insert_one(word_data)
    
    def get_recent_words(self, limit=10):
        return list(self.collection.find().sort("created_at", -1).limit(limit))
    
    def search_words(self, query):
        return list(self.collection.find({
            "$or": [
                {"word": {"$regex": query, "$options": "i"}},
                {"vietnamese_meaning": {"$regex": query, "$options": "i"}},
                {"english_meaning": {"$regex": query, "$options": "i"}}
            ]
        }))
    
    def update_word(self, word_id, word_data):
        word_data['updated_at'] = datetime.now()
        return self.collection.update_one(
            {"_id": ObjectId(word_id)}, 
            {"$set": word_data}
        )
    
    def delete_word(self, word_id):
        return self.collection.delete_one({"_id": ObjectId(word_id)})
    
    def get_all_words(self):
        return list(self.collection.find())
    
    def get_word_by_id(self, word_id):
        return self.collection.find_one({"_id": ObjectId(word_id)})

class ProgressModel:
    def __init__(self, db):
        self.db = db
        self.collection = db.progress
    
    def update_progress(self, word_id, correct):
        existing = self.collection.find_one({"word_id": word_id})
        if existing:
            new_attempts = existing.get('attempts', 0) + 1
            new_correct = existing.get('correct_answers', 0) + (1 if correct else 0)
            
            self.collection.update_one(
                {"word_id": word_id},
                {
                    "$set": {
                        "attempts": new_attempts,
                        "correct_answers": new_correct,
                        "last_reviewed": datetime.now(),
                        "accuracy": (new_correct / new_attempts) * 100
                    }
                }
            )
        else:
            self.collection.insert_one({
                "word_id": word_id,
                "attempts": 1,
                "correct_answers": 1 if correct else 0,
                "last_reviewed": datetime.now(),
                "accuracy": 100 if correct else 0,
                "next_review": datetime.now()
            })