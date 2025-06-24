from datetime import datetime, timedelta
import random

class SpacedRepetition:
    def __init__(self):
        self.reviews = []

    def add_review(self, vocabulary_id, last_reviewed, interval, ease_factor):
        self.reviews.append({
            'vocabulary_id': vocabulary_id,
            'last_reviewed': last_reviewed,
            'interval': interval,
            'ease_factor': ease_factor
        })

    def calculate_next_review(self, review):
        next_review_date = review['last_reviewed'] + timedelta(days=review['interval'])
        return next_review_date

    def update_review(self, vocabulary_id, correct):
        for review in self.reviews:
            if review['vocabulary_id'] == vocabulary_id:
                if correct:
                    review['interval'] = self.calculate_interval(review['interval'], review['ease_factor'])
                    review['ease_factor'] = self.calculate_ease_factor(review['ease_factor'], correct)
                else:
                    review['interval'] = 1  # Reset interval on incorrect answer
                review['last_reviewed'] = datetime.now()
                break

    def calculate_interval(self, current_interval, ease_factor):
        return round(current_interval * ease_factor)

    def calculate_ease_factor(self, current_ease_factor, correct):
        if correct:
            return min(2.5, current_ease_factor + 0.1)
        else:
            return max(1.3, current_ease_factor - 0.1)

    def get_due_reviews(self):
        due_reviews = []
        for review in self.reviews:
            if self.calculate_next_review(review) <= datetime.now():
                due_reviews.append(review)
        return due_reviews

    def get_random_review(self):
        if not self.reviews:
            return None
        return random.choice(self.reviews)