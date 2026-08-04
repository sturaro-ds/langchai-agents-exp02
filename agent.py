from src.tavily_web_search import web_search
from src.mysql_usp_databse import sql_usp
from src.retriever_azure import search_knowledgebase_05

from azure.identity import DefaultAzureCredential
from langchain_azure_ai.chat_models import AzureAIOpenAIApiChatModel
from langchain_azure_ai.retrievers import (
    AzureAISearchRetriever,
    AzureCognitiveSearchRetriever
)
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver

import os
import warnings as ww
ww.filterwarnings('ignore')
from yaspin import yaspin
from dotenv import load_dotenv
load_dotenv()

# FERRAMENTAS MODULADAS
tools = [
    search_knowledgebase_05,
    web_search, 
    sql_usp
]

# LLM COM ENDPOINT DA AZURE FOUNDRY
llm = AzureAIOpenAIApiChatModel(
    project_endpoint=os.getenv('FOUNDRY_PROJ_ENDPOINT'),
    credential=DefaultAzureCredential(),
    model='gpt-5.4-mini'
)

# AGENTE COM FERRAMENTAS + MEMÓRIA DA SESSAO
agente = create_agent(
    model=llm,
    system_prompt='Voce é um assistente pessoal, use suas ferramentas quando necessário.',
    checkpointer=MemorySaver(),
    tools=tools
)


# BANNER NO INICIO DO CHAT NO TERMINAL
def print_banner():
    largura = 48
    borda = "=" * largura
    linha_vazia = "||" + " " * (largura - 4) + "||"

    print(borda)
    print(linha_vazia)
    print("||   🤖  BEM VINDO AO AGENTE STURARO  🤖      ||")
    print(linha_vazia)
    print(borda)


# WORKFLOW
if __name__ == '__main__':

    print_banner()

    while True:

        pergunta = input('\n💬 Insira sua pergunta ou digite QUIT para encerrar: ')

        if pergunta == 'QUIT':
            print('\n😊 Voce digitou QUIT, good bye!\n')
            break

        with yaspin(text='Pensando', color='cyan') as run:

            response = agente.invoke(
                input={
                    'messages': [HumanMessage(content=pergunta)]
                },
                config={'configurable': {'thread_id': '1'}}
            )
            print('\n', response['messages'][-1].text)