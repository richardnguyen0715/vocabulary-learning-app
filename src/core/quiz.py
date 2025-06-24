from pymongo import MongoClient
import random

class Quiz:
    def __init__(self, db):
        self.db = db
        self.questions = []
        self.current_question = None
        self.score = 0

    def load_questions(self):
        # Load questions from the database
        self.questions = list(self.db.quizzes.find())

    def get_random_question(self):
        if not self.questions:
            return None
        self.current_question = random.choice(self.questions)
        return self.current_question

    def check_answer(self, user_answer):
        if self.current_question and user_answer.lower() == self.current_question['answer'].lower():
            self.score += 1
            return True
        return False

    def get_score(self):
        return self.score

    def reset_score(self):
        self.score = 0

    def get_question_type(self):
        if self.current_question:
            return self.current_question['type']
        return None

    def get_choices(self):
        if self.current_question and self.current_question['type'] == 'multiple_choice':
            return self.current_question['choices']
        return []