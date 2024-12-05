from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Load the prompt template
with open("./scripts/prompts/femalebot.txt", "r") as file:
    template = file.read()

# Initialize the model and chain
model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# Context dictionary to maintain user conversations
user_contexts = {}

def handle_chat(user_id, user_input):
    """
    Handles the chat logic for a given user.

    Args:
        user_id (str): Unique identifier for the user.
        user_input (str): User's message to the chatbot.

    Returns:
        str: The chatbot's response.
    """
    global user_contexts

    # Retrieve or initialize the user's context
    context = user_contexts.get(user_id, "")

    # Invoke the model
    result = chain.invoke(
        {
            "context": context,
            "question": user_input,
        }
    )

    # Update the user's context
    user_contexts[user_id] = context + f"\nUser: {user_input}\nAI: {result}"

    return result
