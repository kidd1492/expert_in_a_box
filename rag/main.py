import sys, uuid
from tools_folder.tool_file import db
from agents.ReAct_agent import app
from langchain_core.messages import HumanMessage


def generate_new_thread_id():
    return str(uuid.uuid4())


if __name__ == "__main__":
    args = sys.argv
    thread_arg = args[1] if len(args) > 1 else None

    if thread_arg is None:
        last_thread_id = db.get_last_thread_id()
        if last_thread_id:
            thread_id = last_thread_id
            print(f"No thread_id provided. Using last thread: {thread_id}")
        else:
            thread_id = generate_new_thread_id()
            print(f"No previous thread found. Starting new thread: {thread_id}")
    else:
        thread_id = thread_arg
        print(f"Using provided thread_id: {thread_id}")

    result = db.load_memory(thread_id)
    if not result:
        print(f"No memory found for thread {thread_id}. Starting fresh.")
        app.invoke({'thread_id': thread_id})
    else:
        summary, messages_list = result
        messages = [HumanMessage(content=m) for m in messages_list]
        print(f"Loaded memory for thread {thread_id}")
        app.invoke({"summary": summary, "messages": messages, 'thread_id': thread_id})

