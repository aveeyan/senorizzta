from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

file = open("./scripts/prompts/femalebot.txt", 'r')
template = file.read()
print(template)

model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def conversation_female():
    context = ""
    print("Welcome to the AI ChatBot! Type 'exit' to quit.")
    while 1:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        result = chain.invoke(
            {
            "context": context,
            "question": user_input
            }
        )
        print("Bot: ", result)
        # User Context
        context += f"\nUser: {user_input}\nAI: {result}"

if __name__ == "__main__":
    conversation_female()