from azure.identity import DefaultAzureCredential
from langchain_azure_ai.chat_models import AzureAIOpenAIApiChatModel
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.chat_models.base import init_chat_model
from langchain_core.tools import tool
import pymysql as mysql
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os
load_dotenv()

# MYSQL
db_pass = quote_plus(os.getenv('MYSQL_PASS'))
db_uri = f'mysql+pymysql://sturaro:{db_pass}@127.0.0.1:3306/USP'
db = SQLDatabase.from_uri(db_uri)

# AGENTE SQL COM LLM AZURE FOUNDRY
llm = AzureAIOpenAIApiChatModel(
    project_endpoint=os.getenv('FOUNDRY_PROJ_ENDPOINT'),
    credential=DefaultAzureCredential(),
    model='gpt-5.4-mini'
)

sql_toolkit = SQLDatabaseToolkit(
    db=db, 
    llm=llm
)

agent_sql = create_sql_agent(
    llm=llm,
    toolkit=sql_toolkit,
    prefix='Voce é especialista em SQL e tem acesso ao banco de dados USP',
    verbose=True
)

@tool
def sql_usp(query: str):
    """Acesso ao banco de dados / database USP para querys em SQL"""
    return agent_sql.run(query)