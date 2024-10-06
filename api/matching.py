from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_resumes_to_jd(job_description, resumes):
    vectorizer = TfidfVectorizer()
    resume_texts = [resume['text'] for resume in resumes]
    texts = [job_description] + resume_texts
    
    tfidf_matrix = vectorizer.fit_transform(texts)
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    ranked_resumes = sorted(zip(resumes, cosine_similarities), key=lambda x: x[1], reverse=True)
    return ranked_resumes
