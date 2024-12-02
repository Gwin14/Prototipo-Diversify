from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from ..models import Vaga

def gerar_recomendacoes(vaga_id, top_n=3):
    # Obtém todas as vagas
    vagas = Vaga.objects.all()
    df = pd.DataFrame(list(vagas.values('id', 'title', 'description', 'tags')))

    # Cria uma coluna combinada de texto
    df['texto_combinado'] = df['title'] + " " + df['description']  # Ajuste conforme necessário

    # Definindo stop words personalizadas para o idioma português
    stop_words_portugues = [
        'a', 'o', 'e', 'é', 'de', 'da', 'do', 'em', 'para', 'com', 'por', 'não', 'uma', 'um', 'nas', 'nos', 'as', 'os', 'se', 'que',
        'ao', 'ou', 'na', 'no', 'como', 'dos', 'das', 'depois', 'antes', 'se', 'mas', 'muito', 'também', 'essa', 'essa', 'então',
        'se', 'só', 'essa', 'mesmo', 'quando', 'porque'
    ]

    # Vetorização TF-IDF com stop words em português
    vectorizer = TfidfVectorizer(stop_words=stop_words_portugues)
    tfidf_matrix = vectorizer.fit_transform(df['texto_combinado'])

    # Calcula similaridade
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Obtém o índice da vaga de referência
    idx = df.index[df['id'] == vaga_id][0]

    # Obtém índices das vagas mais similares
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n + 1]

    # Retorna IDs das vagas recomendadas
    recommended_vaga_ids = [df.iloc[i[0]]['id'] for i in sim_scores]
    return Vaga.objects.filter(id__in=recommended_vaga_ids)
