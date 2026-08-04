from tavily.client import TavilyClient
from dotenv import load_dotenv
from typing import List, Dict, Any
from langchain_core.tools import tool

load_dotenv()

# CLIENT
client = TavilyClient()

# BUSCA NA WEB COM API TAVILY
@tool
def web_search(query: str) -> Dict[str, Any]:
    """Busca informacoes na web / internet"""
    resposta = client.search(query=query)
    return resposta['results']
