from sentence_transformers import SentenceTransformer, util

# On charge le modèle UNE SEULE FOIS (au début)
# C'est un modèle léger mais très intelligent
model = SentenceTransformer('all-MiniLM-L6-v2')

def calculer_score_matching(competences_stagiaire, competences_offre):
    """
    Utilise une IA Deep Learning pour comprendre le SENS des phrases.
    """
    
    # 1. On encode les deux textes en vecteurs de nombres (Embeddings)
    # L'IA transforme le sens de la phrase en une liste de chiffres
    embedding_stagiaire = model.encode(competences_stagiaire, convert_to_tensor=True)
    embedding_offre = model.encode(competences_offre, convert_to_tensor=True)
    
    # 2. On calcule la similarité Cosine entre les deux sens
    # Le résultat est entre 0 et 1 (ex: 0.7532)
    score_brut = util.cos_sim(embedding_stagiaire, embedding_offre)
    
    # 3. On convertit en pourcentage propre (ex: 75.32)
    score_final = score_brut.item() * 100
    
    return round(score_final, 2)