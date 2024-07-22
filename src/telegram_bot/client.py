from src.telegram_bot.config import CONFIG
from langchain.chains.summarize import load_summarize_chain 
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Literal

class ChatbotClient:
    def __init__(self,chatbot:str = Literal['openai','google']):
        if chatbot == 'openai':
            self.llm = ChatOpenAI(
                model=CONFIG.OPENAI_MODEL,
                temperature=0.5,
                max_token=None,
                timeout=None,
                max_retries=2
            )
        elif chatbot == 'google':
            self.llm = ChatGoogleGenerativeAI(
                model=CONFIG.GEMINI_MODEL,
                temperature=0.5,
                max_tokens=None,
                timeout=None,
                max_retries=2,
            )

    def chat(self, text: str) -> str:
        messages = [
            (
                "system",
                "You are a helpful assistant. Please give the best anser",
            ),
            ("human", f"{text}"),
        ]
        response = self.llm.invoke(messages)
        return response.content


class SummarizationClient:
    def __init__(self,chatbot:str = Literal['openai','google']):
        if chatbot == 'openai':
            self.llm = ChatOpenAI(
                model=CONFIG.OPENAI_MODEL,
                temperature=0
            )
        elif chatbot == 'google':
            self.llm = ChatGoogleGenerativeAI(
                model=CONFIG.GEMINI_MODEL,
                temperature=0
            )
        self.chain = load_summarize_chain(self.llm, chain_type="stuff")

    def load(self, url: str) -> str:
        docs = WebBaseLoader(url).load()
        
        return self.chain.invoke(docs)


        
