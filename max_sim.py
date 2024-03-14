import spacy
from nltk.corpus import wordnet as wn

def get_synonyms(word):
    synonyms = set()
    for synset in wn.synsets(word):
        for lemma in synset.lemmas():
            synonyms.add(lemma.name())
    return synonyms

def calculate_similarity(text1, text2):
    nlp = spacy.load("en_core_web_lg")
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    similarity = doc1.similarity(doc2)
    return similarity

def calculate_synonym_similarity(text1, text2):
    nlp = spacy.load("en_core_web_md")
    
    def file_to_tokens(text):
        doc = nlp(text)
        tokens = [token.text for token in doc if not token.is_stop and token.is_alpha]
        return tokens
    
    tokens1 = file_to_tokens(text1)
    tokens2 = file_to_tokens(text2)
    
    synonyms1 = set()
    synonyms2 = set()
    
    for token in tokens1:
        synonyms = get_synonyms(token)
        synonyms1.update(synonyms)
    
    for token in tokens2:
        synonyms = get_synonyms(token)
        synonyms2.update(synonyms)
    
    intersection = len(synonyms1.intersection(synonyms2))
    union = len(synonyms1.union(synonyms2))
    similarity = intersection / union if union > 0 else 0
    
    return similarity

if __name__ == "__main__":
    with open("file1.txt", "r") as f1, open("file2.txt", "r") as f2:
        text1 = f1.read()
        text2 = f2.read()
    
    spacy_similarity = calculate_similarity(text1, text2)
    synonym_similarity = calculate_synonym_similarity(text1, text2)
    
    # Scale the similarity to a range from 0 to 10
    spacy_scaled = round(spacy_similarity * 10)
    synonym_scaled = round(synonym_similarity * 10)
    
    # Choose the maximum scaled similarity
    max_similarity = max(spacy_scaled, synonym_scaled)
    
    print("Similarity using spaCy (scaled):", spacy_scaled)
    print("Similarity using synonyms (scaled):", synonym_scaled)
    print("Maximum Similarity (scaled):", max_similarity)
