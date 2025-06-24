import requests
import json
from typing import Dict, Optional

class DictionaryService:
    def __init__(self):
        self.base_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
        self.timeout = 3  # 3 seconds timeout
    
    def get_word_info(self, word: str) -> Dict:
        """
        Get English meaning and pronunciation for a word
        """
        try:
            response = requests.get(f"{self.base_url}{word.lower()}", timeout=self.timeout)
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
            
            # If API fails, return empty data
            return self._get_fallback_data()
            
        except requests.exceptions.Timeout:
            print(f"Timeout when fetching word info for: {word}")
            return self._get_fallback_data()
        except requests.exceptions.ConnectionError:
            print(f"Connection error when fetching word info for: {word}")
            return self._get_fallback_data()
        except Exception as e:
            print(f"Error fetching word info for {word}: {e}")
            return self._get_fallback_data()
    
    def _get_fallback_data(self) -> Dict:
        """Return empty data when API fails"""
        return {
            'english_meaning': "",
            'pronunciation': "",
            'part_of_speech': "",
            'example': ""
        }