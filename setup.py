from setuptools import setup, find_packages

setup(
    name="VocabularyLearningApp",
    version="1.0.0",
    author="Your Name",
    description="A vocabulary learning application with flashcards and quizzes",
    packages=find_packages(),
    install_requires=[
        "pymongo>=4.6.0",
        "requests>=2.31.0",
    ],
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'vocabulary-app=main:main',
        ],
    },
)