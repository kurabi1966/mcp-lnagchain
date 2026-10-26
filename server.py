from dotenv import load_dotenv

load_dotenv()

from mcp.server.mcpserver import MCPServer

from tavily import TavilyClient
from typing import Dict, Any
from requests import get

mcp = MCPServer("mcp-server")

tavily_client = TavilyClient()

@mcp.tool()
def search_web(query: str) -> Dict[str, Any]:
  """Search the web for information"""
  result = tavily_client.search(query=query)
  return result

@mcp.resource("github.com://langchain-ai/langchain-mcp-adapters/blob/main/README.md")
def github_file():
  """
  Resource for accessing langchain-ai/langchain-mcp-adapters/README.md file
  """
  
  url = f"https://github.com/langchain-ai/langchain-mcp-adapters/blob/main/README.md"
  try:
      resp = get(url)
      return resp.text
  except Exception as e:
    return f"Error: {str(e)}"
  
@mcp.prompt()
def prompt():
  """
  Analyze data from a langchain-ai repo file with comperhensive insight
  """
  
  return """
  You are a helpful assistent that answer user questions about LangChain, LangGraph and LangSmith.
  
  You can use the following tools/resources to answer user question:
  - search_web: Search the web for information
  - github_file: Acces the langchain-ai repo files
  
  If the user asks a question that is not related to LangChain, LangGraph, LangSmith, you should say 
  "I'am sorry, I'am specilized in answering questions related to LangChain eco-system."
  
  You may try multiple tool and resources calls to answer the user's question.
  
  You may also ask clarifications to the user to better understand thier question.  
  """
  
if __name__ == "__main__":
  mcp.run(transsport="stdio")
  
  

    