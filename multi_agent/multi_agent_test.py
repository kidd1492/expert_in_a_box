from langchain_core.messages import SystemMessage
from langchain_ollama import ChatOllama
from ReAct_agent import running_agent

model = ChatOllama(model="llama3.2:3b")


def outline():
  
    system_prompt = SystemMessage(content="""You are an assistant. Given the user's Topic:
                                    1. generate an step by step outline for a detailed blog post about the topic, 2. the outline should be a teachable step by step guide. 
                                    3. search_terms: A list of search terms to look up for better understanding of the topic
                                       search terms for the vectorstore dealing with langgraph, wikipedia for any other.   User's Topic:""")
    user_input = input("Enter a Topic: ")
    result = model.invoke(f"{system_prompt} {user_input}")

    with open("output.txt", "a", encoding="utf-8") as output:
        output.write(f"inputs: {system_prompt} {user_input}\n")
        output.write(f"outline results: {result.content}\n")

    print("Outline sent to agent.", "\n")
    return result.content


if __name__ == "__main__":
    result = outline()
    #running_agent(result)
