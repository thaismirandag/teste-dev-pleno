import logging
from openai import AuthenticationError, OpenAIError
from langchain_openai import OpenAI
from langchain.chains.llm import LLMChain
from .prompts import petlove_assistant_prompt
from .config import Config


class AssistantPetLoveService:
    def __init__(self):
        self.config = Config()
        self.api_key = self.config.openai_api_key
        if self.api_key:
            try:
                self.llm = OpenAI(model='gpt-3.5-turbo-instruct',
                 temperature=0, max_tokens=500, api_key=self.api_key)
                self.llm_chain = LLMChain(llm=self.llm, prompt=petlove_assistant_prompt)
            except Exception as e:
                logging.error("Erro ao inicializar OpenAI %s:", e)
                raise
        else:
            raise ValueError("Chave da API da OpenAI não encontrada!")

    def get_response(self, question: str) -> str:
        try:
            response = self.llm_chain.invoke({"question": question})
            return response
        except AuthenticationError as e:
            logging.error("Erro de autenticação: %s", e)
            raise
        except OpenAIError as e:
            logging.error("Erro para obter uma resposta: %s", e)
            raise
        except Exception as e:
            logging.error("Erro inesperado para obter uma resposta: %s", e)
            raise

    def format_response(self, data):
        answer = data.get("text", "Resposta não encontrada")
        return f"{answer}"
