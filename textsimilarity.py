import math
import string
from collections import Counter

STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", 
    "is", "am", "are", "was", "were", "be", "been",
    "in", "on", "at", "to", "for", "of", "with",
    "it", "this", "that", "i", "you", "he", "she", "we", "they"
}

def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    
    filtered_words = [word for word in words if word not in STOP_WORDS]
    
    return filtered_words

def get_cosine_similarity(text1, text2):
    words1 = clean_text(text1)
    words2 = clean_text(text2)

    all_words = set(words1).union(set(words2))
    
    vec1 = Counter(words1)
    vec2 = Counter(words2)

    
    dot_product = 0
    for word in all_words:
        dot_product += vec1[word] * vec2[word]

    magnitude1 = math.sqrt(sum(vec1[word]**2 for word in all_words))
    magnitude2 = math.sqrt(sum(vec2[word]**2 for word in all_words))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)

text1 = """
Computer science is the study of computation, information, and automation. 
Computer science spans theoretical disciplines from algorithms, theory of computation, 
and information theory to practical disciplines including the design and implementation 
of hardware and software. Computer science is generally considered an area of academic 
research and distinct from computer programming.
"""
text2 = """
The field of Computer Science involves studying automation, information, and computation. 
It covers a wide range of theoretical subjects like algorithms and information theory, 
as well as practical areas such as software and hardware design. Usually, computer science 
is seen as an academic research field that is separate from just writing computer programs.
"""
similarity = get_cosine_similarity(text1, text2)
print(f"Similariry : {similarity * 100:.2f}%")
