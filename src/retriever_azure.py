import os
import asyncio
from datetime import datetime, timedelta
from azure.identity import DefaultAzureCredential
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.tools import tool

_credential = DefaultAzureCredential()
_cached_token = None
_token_expiry = datetime.min

# GERA O TOKEN TEMPORARIO
def _get_token() -> str:
    global _cached_token, _token_expiry
    if datetime.now() >= _token_expiry:
        result = _credential.get_token("https://search.azure.com/.default")
        _cached_token = result.token
        _token_expiry = datetime.fromtimestamp(result.expires_on) - timedelta(minutes=5)
    return _cached_token

# FUNCAO DO RETRIEVER
async def _retrieve_from_kb(query: str) -> str:
    client = MultiServerMCPClient({
        "knowledgebase-05": {
            "transport": "streamable_http",
            "url": os.getenv('MCP_URL_SRCH'),
            "headers": {"Authorization": f"Bearer {_get_token()}"},
        }
    })
    async with client.session("knowledgebase-05") as session:
        result = await session.call_tool("knowledge_base_retrieve", {"queries": [query]})
    textos = [bloco.text for bloco in result.content if hasattr(bloco, "text")]
    return "\n\n".join(textos)

@tool
def search_knowledgebase_05(query: str) -> str:
    """Busca informações na base de conhecimento (condomínio Joy Cambuci) via Foundry IQ."""
    return asyncio.run(_retrieve_from_kb(query))