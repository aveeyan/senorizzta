import cv2
from PIL import Image
import pytesseract
import ollama
from langchain_core.prompts import ChatPromptTemplate

# Image Text Extractor Class
class ImageTextExtractor:
    def __init__(self):
        pass

    def preprocess_image(self, image_path):
        """
        Preprocess the image for text extraction.
        """
        try:
            image = cv2.imread(image_path, cv2.IMREAD_COLOR)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, thresh_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)
            preprocessed_path = "./scripts/preprocessed/preprocessed_image.png"
            cv2.imwrite(preprocessed_path, thresh_image)
            return preprocessed_path
        except Exception as e:
            print(f"Error during preprocessing: {e}")
            return None

    def extract_text(self, image_path):
        """
        Extract text from an image using Tesseract.
        """
        try:
            preprocessed_path = self.preprocess_image(image_path)
            if not preprocessed_path:
                return None

            image = Image.open(preprocessed_path)
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            print(f"Error during text extraction: {e}")
            return None

class Assistbot:
    def __init__(self, user_id, gender):
        self.model = "llama3"
        self.user_contexts = {}
        self.gender = gender
        self.user_id = user_id

    def load_prompt(self):
        file_path = f"./scripts/prompts/aiassist.txt"
        try:
            with open(file_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            raise ValueError(f"Prompt file for gender '{self.gender}' not found at {file_path}")

    def handle_chat(self, user_input):
        """
        Generate a response based on the input text and user context.
        """
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

# Example Usage
if __name__ == "__main__":
    # Step 1: Extract text from the image
    image_file = "./scripts/test_chat.png"
    text_extractor = ImageTextExtractor()
    extracted_text = text_extractor.extract_text(image_file)

    if extracted_text:
        print("Extracted Text:")
        print(extracted_text)

        # Step 2: Pass the text to the chatbot for a response
        chatbot = Assistbot(user_id="user123", gender="male")  # Example user and gender
        response = chatbot.handle_chat(extracted_text)
        print("Chatbot Response:")
        print(response)
    else:
        print("No text could be extracted from the image.")
