import ollama
from langchain_core.prompts import ChatPromptTemplate

class Chatbot:
    def __init__(self, user_id, gender):
        self.model = "llama3"
        self.user_contexts = {}
        self.gender = gender
        self.user_id = user_id

    def load_prompt(self):
        file_path = f"./scripts/prompts/{self.gender}bot.txt"
        try:
            with open(file_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            raise ValueError(f"Prompt file for gender '{self.gender}' not found at {file_path}")

    def handle_chat(self, user_input):
        try:
            template = self.load_prompt()
        except ValueError as e:
            return str(e)

        prompt = ChatPromptTemplate.from_template(template)
        formatted_prompt = prompt.format(context=self.user_contexts.get(self.user_id, ""), question=user_input)

        try:
            result = ollama.generate(model=self.model, prompt=formatted_prompt)
        except Exception as e:
            return f"Error generating response: {e}"

        context = self.user_contexts.get(self.user_id, "") + f"\nUser: {user_input}\nAI ({self.gender.capitalize()}): {result}"
        self.user_contexts[self.user_id] = context
        return result