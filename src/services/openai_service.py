# src/services/openai_service.py
import openai
from src.config import Settings
from src.services.vector_service import VectorService

class OpenAIService:
    def __init__(self, settings: Settings):
        self.settings = settings
        openai.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL

    async def process_query(
        self,
        query: str,
        namespace: str,
        vector_service: VectorService
    ) -> str:
        try:
            # Get relevant context from vector store
            context = vector_service.get_relevant_context(query, namespace)

            # Prepare prompt
            prompt = self._prepare_prompt(query, context)

            # Get response from OpenAI
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for AMC."},
                    {"role": "user", "content": prompt}
                ]
            )

            return response.choices[0].message.content

        except Exception as e:
            raise Exception(f"Error processing query: {str(e)}")

    def _prepare_prompt(self, query: str, context: str) -> str:
        return f"""
        Context: {context}

        Question: {query}

        Please provide a helpful response based on the context above.
        """
