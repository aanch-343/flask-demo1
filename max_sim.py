# import spacy
# from nltk.corpus import wordnet as wn

# def get_synonyms(word):
#     synonyms = set()
#     for synset in wn.synsets(word):
#         for lemma in synset.lemmas():
#             synonyms.add(lemma.name())
#     return synonyms

# def calculate_similarity(text1, text2):
#     nlp = spacy.load("en_core_web_lg")
#     doc1 = nlp(text1)
#     doc2 = nlp(text2)
#     similarity = doc1.similarity(doc2)
#     return similarity

# def calculate_synonym_similarity(text1, text2):
#     nlp = spacy.load("en_core_web_md")
    
#     def file_to_tokens(text):
#         doc = nlp(text)
#         tokens = [token.text for token in doc if not token.is_stop and token.is_alpha]
#         return tokens
    
#     tokens1 = file_to_tokens(text1)
#     tokens2 = file_to_tokens(text2)
    
#     synonyms1 = set()
#     synonyms2 = set()
    
#     for token in tokens1:
#         synonyms = get_synonyms(token)
#         synonyms1.update(synonyms)
    
#     for token in tokens2:
#         synonyms = get_synonyms(token)
#         synonyms2.update(synonyms)
    
#     intersection = len(synonyms1.intersection(synonyms2))
#     union = len(synonyms1.union(synonyms2))
#     similarity = intersection / union if union > 0 else 0
    
#     return similarity

# if __name__ == "__main__":
#     with open("file1.txt", "r") as f1, open("file2.txt", "r") as f2:
#         text1 = f1.read()
#         text2 = f2.read()
    
#     spacy_similarity = calculate_similarity(text1, text2)
#     synonym_similarity = calculate_synonym_similarity(text1, text2)
    
#     # Scale the similarity to a range from 0 to 10
#     spacy_scaled = round(spacy_similarity * 10)
#     synonym_scaled = round(synonym_similarity * 10)
    
#     # Choose the maximum scaled similarity
#     max_similarity = max(spacy_scaled, synonym_scaled)
    
#     # print("Similarity using spaCy (scaled):", spacy_scaled)
#     # print("Similarity using synonyms (scaled):", synonym_scaled)

import spacy
import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from collections import defaultdict

nltk.download('punkt')
nltk.download('wordnet')
nlp = spacy.load("en_core_web_lg")

def preprocess_text(text):
    text = text.lower().strip()
    text = ''.join([char for char in text if char.isalnum() or char.isspace()])
    return text

def replace_numerical_with_token(tokens):
    return ['NUM' if token.isdigit() else token for token in tokens]

def get_synonyms(word):
    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return synonyms

def get_sentence_synonyms(tokens):
    synonyms_dict = defaultdict(set)
    for token in tokens:
        synonyms = get_synonyms(token.lower())
        synonyms_dict[token.lower()].update(synonyms)
    return synonyms_dict

def get_sentence_tokens(text):
    tokens = [token.lower() for token in word_tokenize(text) if token.isalpha()]
    return tokens

def calculate_contextual_similarity(text1, text2):
    text1 = preprocess_text(text1)
    text2 = preprocess_text(text2)
    
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    
    threshold = 0.74
    similarity = doc1.similarity(doc2)
    if similarity > threshold:
        return similarity
    else:
        return 0

def calculate_synonym_similarity(text1, text2):
    tokens1 = get_sentence_tokens(text1)
    tokens2 = get_sentence_tokens(text2)

    synonyms1 = get_sentence_synonyms(replace_numerical_with_token(tokens1))
    synonyms2 = get_sentence_synonyms(replace_numerical_with_token(tokens2))

    intersection = sum(len(synonyms1[word].intersection(synonyms2[word])) for word in synonyms1 if word in synonyms2)
    union = sum(len(synonyms1[word].union(synonyms2[word])) for word in synonyms1) + sum(len(synonyms2[word]) for word in synonyms2 if word not in synonyms1)
    similarity = intersection / union if union > 0 else 0
    return similarity

def combined_similarity(text1, text2):
    # If texts have the same length
    if len(text1.split()) == len(text2.split()):
        contextual_sim = calculate_contextual_similarity(text1, text2)
        synonym_sim = calculate_synonym_similarity(text1, text2)
        print("spacy",contextual_sim)
        print("nltk",synonym_sim)
        average_similarity = (contextual_sim + synonym_sim) / 2
        return average_similarity, average_similarity  # Note the comma to make it a tuple
    elif abs(len(text1.split()) - len(text2.split())) > max(len(text1.split()), len(text2.split())) * 0.5:
        contextual_sim = calculate_contextual_similarity(text1, text2)
        synonym_sim = calculate_synonym_similarity(text1, text2)
        print("spacy",contextual_sim)
        print("nltk",synonym_sim)
        # If texts have a huge difference in lengt
        average_similarity = (calculate_contextual_similarity(text1, text2) + calculate_synonym_similarity(text1, text2)) / 2
        return average_similarity, average_similarity 
    elif len(text1.split('.')) >= 3 and len(text2.split('.')) >= 3:
        contextual_sim = calculate_contextual_similarity(text1, text2)
        synonym_sim = calculate_synonym_similarity(text1, text2)
        print("spacy",contextual_sim)
        print("nltk",synonym_sim)
        # If both texts have 3 or more sentences
        average_similarity = (calculate_contextual_similarity(text1, text2) + calculate_synonym_similarity(text1, text2)) / 2
        
        return average_similarity, average_similarity
    else:
        contextual_sim = calculate_contextual_similarity(text1, text2)
        synonym_sim = calculate_synonym_similarity(text1, text2)
        print("spacy",contextual_sim)
        print("nltk",synonym_sim)
        return contextual_sim, synonym_sim



