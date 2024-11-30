import logging
from app.models.model import PhiModelSingleton, TextChunking ,get_answer_from_cv

# Initialiser le logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_answer(question: str, cv_text: str) -> str:
    """
    Générer une réponse à partir d'une question et d'un texte de CV.
    Utilise PhiModelSingleton et TextChunking pour le traitement et l'extraction contextuelle.

    Args:
        question (str): La question posée.
        cv_text (str): Le texte du CV utilisé comme contexte.

    Returns:
        str: La réponse générée ou un message d'erreur.
    """
    try:
        # Validation des entrées
        if not question.strip():
            logger.warning("La question est vide ou invalide : '%s'", question)
            return "La question fournie est vide ou invalide."
        
        if not cv_text.strip():
            logger.warning("Le texte du CV est vide ou invalide : '%s'", cv_text)
            return "Le texte du CV est vide ou invalide."

        # Initialisation des outils nécessaires
        phi_model = PhiModelSingleton()
        chunker = TextChunking()

        # Division du texte du CV en chunks
        chunks = chunker.chunk_text(cv_text)
        if not chunks:
            logger.warning("Aucun chunk généré à partir du texte du CV.")
            return "Le texte du CV est trop court pour être analysé."

        # Création de l'index FAISS pour les chunks
        chunker.build_index(chunks)

        # Trouver les chunks les plus pertinents pour la question
        similar_chunks = chunker.find_most_similar(question, chunks)
        if not similar_chunks:
            logger.warning("Aucun chunk pertinent trouvé pour la question.")
            return "Impossible de trouver une réponse pertinente à partir du texte fourni."

        # Fusionner les chunks les plus pertinents pour former le contexte
        context = " ".join(similar_chunks)

        # Générer la réponse à l'aide du modèle
        answer = get_answer_from_cv(question, context)

        # Vérifier si la réponse générée est vide
        if not answer.strip():
            logger.warning("La réponse générée est vide.")
            return "Aucune réponse générée. Veuillez reformuler votre question ou fournir un CV plus détaillé."

        logger.info("Réponse générée avec succès.")
        return answer

    except Exception as e:
        logger.error(f"Erreur dans get_answer : {str(e)}")
        return "Une erreur est survenue lors de la génération de la réponse."



