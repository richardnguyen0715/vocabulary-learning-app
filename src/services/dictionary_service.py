import requests
import json
from typing import Dict, Optional

class DictionaryService:
    def __init__(self):
        self.base_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
    
    def get_word_info(self, word: str) -> Dict:
        """
        Get English meaning and pronunciation for a word
        """
        try:
            response = requests.get(f"{self.base_url}{word.lower()}")
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    word_data = data[0]
                    
                    # Extract meanings
                    meanings = []
                    if 'meanings' in word_data:
                        for meaning in word_data['meanings']:
                            part_of_speech = meaning.get('partOfSpeech', '')
                            definitions = meaning.get('definitions', [])
                            if definitions:
                                meanings.append({
                                    'part_of_speech': part_of_speech,
                                    'definition': definitions[0].get('definition', ''),
                                    'example': definitions[0].get('example', '')
                                })
                    
                    # Extract pronunciation
                    pronunciation = ""
                    if 'phonetics' in word_data:
                        for phonetic in word_data['phonetics']:
                            if 'text' in phonetic and phonetic['text']:
                                pronunciation = phonetic['text']
                                break
                    
                    return {
                        'english_meaning': meanings[0]['definition'] if meanings else "",
                        'pronunciation': pronunciation,
                        'part_of_speech': meanings[0]['part_of_speech'] if meanings else "",
                        'example': meanings[0]['example'] if meanings else ""
                    }
            return {}
        except Exception as e:
            print(f"Error fetching word info: {e}")
            return {}