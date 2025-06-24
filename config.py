DATABASE_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "vocabulary_learning_app"

# Application settings
APP_TITLE = "Vocabulary Learning App"
APP_VERSION = "1.0.0"

# Collections
VOCABULARY_COLLECTION = "vocabulary"
PROGRESS_COLLECTION = "progress"
QUIZ_RESULTS_COLLECTION = "quiz_results"

# Flashcard settings
FLASHCARD_INTERVAL = 24  # hours
FLASHCARD_LIMIT = 10  # number of flashcards to review at once

# Quiz settings
QUIZ_TIME_LIMIT = 300  # seconds
MULTIPLE_CHOICE_OPTIONS = 4  # number of options for multiple choice questions

# Progress tracking settings
PROGRESS_TRACKING_ENABLED = True

# Import/Export settings
IMPORT_EXPORT_FORMATS = ["csv", "json"]  # supported formats for import/export

# Parts of speech options
PARTS_OF_SPEECH = [
    "Noun", "Verb", "Adjective", "Adverb", "Pronoun", 
    "Preposition", "Conjunction", "Interjection", "Article"
]