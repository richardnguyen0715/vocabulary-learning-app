def search_vocabulary(vocabulary_list, search_term):
    """
    Search for vocabulary entries that match the search term.
    
    Parameters:
    vocabulary_list (list): A list of vocabulary entries.
    search_term (str): The term to search for in the vocabulary entries.
    
    Returns:
    list: A list of vocabulary entries that match the search term.
    """
    return [entry for entry in vocabulary_list if search_term.lower() in entry.lower()]

def search_by_category(vocabulary_list, category):
    """
    Search for vocabulary entries by category.
    
    Parameters:
    vocabulary_list (list): A list of vocabulary entries.
    category (str): The category to filter vocabulary entries by.
    
    Returns:
    list: A list of vocabulary entries that belong to the specified category.
    """
    return [entry for entry in vocabulary_list if entry.category == category]