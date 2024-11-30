from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from sentence_transformers import SentenceTransformer
import faiss
import torch
import logging

# Initialiser le logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class PhiModelSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            try:
                # Initialisation du tokenizer et du modèle
                cls._instance.tokenizer = AutoTokenizer.from_pretrained(
                    "microsoft/Phi-3.5-mini-instruct",
                    trust_remote_code=True
                )
                model = AutoModelForCausalLM.from_pretrained(
                    "microsoft/Phi-3.5-mini-instruct",
                    device_map="auto" if torch.cuda.is_available() else None,
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                    trust_remote_code=True
                )

                # Configuration du pipeline
                cls._instance.pipeline = pipeline(
                    "text-generation",
                    model=model,
                    tokenizer=cls._instance.tokenizer,
                    temperature=0.7,
                    top_k=10,
                    max_new_tokens=250
                )
            except Exception as e:
                raise RuntimeError(f"Erreur lors de l'initialisation du modèle : {str(e)}")
        return cls._instance

    def generate_answer(self, question: str, context: str, max_tokens: int = 1500) -> str:
        """
        Générer une réponse concise et précise en utilisant un contexte donné.
        """
        try:
            # Vérifier que le contexte et la question sont valides
            if not context.strip():
                logger.warning("Le contexte est vide ou invalide.")
                return "Contexte insuffisant pour générer une réponse."
            
            if not question.strip():
                logger.warning("La question est vide ou invalide.")
                return "Question insuffisante pour générer une réponse."

            # Prompt strict et directif
            prompt_template = """
    Contexte :
    {context}

    Question :
    {question}

    Répondez de manière concise, précise et orientée vers la question posée. 
    Faites en sorte que la réponse soit directement utile et sans éléments superflus.
    Réponse :
    """
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )

            if not hasattr(self._instance, 'pipeline') or not self._instance.pipeline:
                raise RuntimeError("Le pipeline n'a pas été initialisé correctement.")

            # Création du LLM
            llm = HuggingFacePipeline(pipeline=self._instance.pipeline)
            chain = LLMChain(llm=llm, prompt=prompt)

            # Génération de la réponse
            response = chain.run(question=question, context=context).strip()
            print(response)

            # Nettoyage de la réponse

            if "Question :" in response:
                response = response.split("Question :")[1].strip()
                
            if "Réponse :" in response:
                response = response.split("Réponse :")[1].strip()


            # Journalisation de la réponse
            logger.info(f"Réponse générée pour la question '{question}': {response}")
            
            # Validation de la réponse générée
            if not response or len(response) < 5:
                logger.warning("La réponse générée semble insuffisante.")
                return "La réponse générée est insuffisante. Essayez de reformuler la question ou d'ajouter plus de contexte."

            return response

        except Exception as e:
            error_message = f"Erreur lors de la génération de la réponse : {str(e)}"
            logger.error(error_message)
            return "Une erreur est survenue lors de la génération de la réponse."


class TextChunking:
    def __init__(self, chunk_size=200):
        self.chunk_size = chunk_size
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None

    def chunk_text(self, text: str) -> list:
        """
        Diviser un texte en chunks de taille spécifiée.
        """
        words = text.split()
        chunks = [' '.join(words[i:i+self.chunk_size]) for i in range(0, len(words), self.chunk_size)]
        return chunks

    def build_index(self, chunks: list):
        """
        Construire un index FAISS pour les embeddings des chunks.
        """
        embeddings = self.embedding_model.encode(chunks, convert_to_tensor=True).cpu().numpy()
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        return embeddings

    def find_most_similar(self, question: str, chunks: list, top_k=3) -> list:
        """
        Trouver les chunks les plus pertinents pour une question.
        """
        question_embedding = self.embedding_model.encode([question], convert_to_tensor=True).cpu().numpy()
        distances, indices = self.index.search(question_embedding, top_k)
        similar_chunks = [chunks[i] for i in indices[0]]
        return similar_chunks


def get_answer_from_cv(question: str, cv_text: str) -> str:
    """
    Obtenir une réponse concise et exacte à partir d'un CV en utilisant PhiModelSingleton et FAISS.
    """
    try:
        # Initialiser le modèle
        phi_model = PhiModelSingleton()

        # Diviser et indexer le CV en chunks
        chunker = TextChunking()
        chunks = chunker.chunk_text(cv_text)
        chunker.build_index(chunks)

        # Identifier les chunks les plus pertinents
        similar_chunks = chunker.find_most_similar(question, chunks)
        context = " ".join(similar_chunks)

        # Générer une réponse concise
        answer = phi_model.generate_answer(question, context, max_tokens=1500)
        return answer

    except Exception as e:
        logger.error(f"Erreur dans get_answer_from_cv : {str(e)}")
        return "Une erreur est survenue lors de la génération de la réponse."
