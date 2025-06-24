from pymongo import MongoClient

class Vocabulary:
    def __init__(self, db_uri, db_name):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.collection = self.db['vocabulary']

    def add_word(self, word, meaning):
        self.collection.insert_one({'word': word, 'meaning': meaning})

    def edit_word(self, word_id, new_word, new_meaning):
        self.collection.update_one(
            {'_id': word_id},
            {'$set': {'word': new_word, 'meaning': new_meaning}}
        )

    def delete_word(self, word_id):
        self.collection.delete_one({'_id': word_id})

    def get_all_words(self):
        return list(self.collection.find())

    def search_word(self, query):
        return list(self.collection.find({'word': {'$regex': query, '$options': 'i'}}))