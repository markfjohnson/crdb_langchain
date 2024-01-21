from langchain_community.llms import LlamaCpp
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain.sql_database import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from urllib.parse import quote


def get_schema( db_sql):
    return db.get_table_info()

def run_query(db):
    return db.get_table_info()

# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
pg_uri = "cockroachdb://root:%s@192.168.2.91:26257/movr?sslmode=disable" % quote('password')
llm = LlamaCpp(
    model_path="/Users/markjohnson/llama/llama.cpp/models/7B/ggml-model-q4_0.bin",
    temperature=0.75,
    max_tokens=2000,
    top_p=1,
    # llama_new_context_with_model=1024,
    context_window=4816,
    n_ctx=4816,
    callback_manager=callback_manager,
    verbose=False,  # Verbose is required to pass to the callback manager
)
db = SQLDatabase.from_uri(pg_uri)
print("Tables available for query")
print(db.get_usable_table_names())
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=False,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)
PROMPT = """ 
Given an input question, first create a syntactically correct postgresql query to run,  
then look at the results of the query and return the answer.  
The question: {question}
"""

question= "How many users are there?"
agent_executor.invoke(PROMPT.format(question=question))
# template = """Based on the table schema below, question, sql query, and sql response, write a natural language response:
# {schema}
#
