from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.llms import LlamaCpp
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain.prompts.prompt import PromptTemplate
from urllib.parse import quote


# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
pg_uri = "cockroachdb://root:%s@192.168.2.91:26257/movr?sslmode=disable" % quote('password')
llm = LlamaCpp(
    model_path="/Users/markjohnson/llama/llama.cpp/models/7B/ggml-model-q4_0.bin",
    temperature=0.75,
    max_tokens=2000,
    top_p=1,
    context_window=4816,
    n_ctx=4816,
    callback_manager=callback_manager,
    verbose=False,  # Verbose is required to pass to the callback manager
)
llm.client.verbose = False
# _DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
# Use the following format:
#
# Question: "Question here"
# SQLQuery: "SQL Query to run"
# SQLResult: "Result of the SQLQuery"
# Answer: "Final answer here"
#
# Only use the following tables:
#
# {table_info}
#
# If someone asks for the table foobar, they really mean the employee table.
#
# Question: {input}"""
#
# PROMPT = PromptTemplate(
#     input_variables=["input", "table_info", "dialect"], template=_DEFAULT_TEMPLATE
# )
db = SQLDatabase.from_uri(pg_uri, include_tables=["rides","users"])
db_chain = SQLDatabaseChain.from_llm(llm, db, return_sql=False, verbose=False)
db_chain.invoke("Create a csv list of the 10 most common rides cities? ")
