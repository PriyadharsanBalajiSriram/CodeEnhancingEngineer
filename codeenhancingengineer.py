!pip install -U langgraph langsmith
from google.colab import userdata
from getpass import getpass
import os
os.environ["GOOGLE_API_KEY"] = getpass("Enter your Google API Key: ")

from typing import TypedDict
class State(TypedDict):
  code:str
  optimisedcode:str

from langgraph.graph import StateGraph, START,END
from langgraph.graph.message import add_messages
from langchain_core.prompts import ChatPromptTemplate

!pip install google-ai-generativelanguage==0.6.15
!pip install -qU \
langchain-google-genai==2.1.4 \
  langgraph==0.4.5 \
  python-dotenv \
  google-ai-generativelanguage==0.6.18 \
  filetype \
  ormsgpack

from langchain_google_genai import ChatGoogleGenerativeAI
llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash")

workflow=StateGraph(State)

def optimizernode(state:State)->State:
  print("\n  optimizing code by leveraging llm....")
  prompt=ChatPromptTemplate.from_template(
      """You are a pro coder,you have to optimize the code until it reaches convergence :This is the code {Code}"""
  )
  chain=prompt|llm
  optimizernodecode=chain.invoke({"Code":state["code"]})
  return {
        "code": state["code"],
        "optimisedcode": optimizernodecode.content if hasattr(optimizernodecode, "content") else str(optimizernodecode)
    }

workflow.add_node("Thejarvis",optimizernode)
workflow.add_edge(START,"Thejarvis")
workflow.add_edge("Thejarvis",END)
app=workflow.compile()

querycode="""def add(a:int,b:int):
return_a_plus_b"""
result=app.invoke({"code":querycode})
print("\n result getting printed")
print(result)
