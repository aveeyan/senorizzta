from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Dictionary to store user-selected genders for pickup line generation
user_genders = {}

# Define a function to load and update the prompt template
def load_template(gender):
    """
    Loads and modifies the prompt template based on the gender chosen.
    
    Args:
        gender (str): The gender ('male' or 'female') for the pickup line.
    
    Returns:
        str: The updated template with gender-specific content.
    """
    with open("./scripts/prompts/rizzgenerator.txt", "r") as file:
        template = file.read()

    # Replace the gender placeholder in the template
    if gender == "female":
        template = template.replace("{gender}", "she")  # or any gender-specific terms for females
    else:
        template = template.replace("{gender}", "he")  # or any gender-specific terms for males

    return template

# Initialize the model
model = OllamaLLM(model="llama3")

def generate_pickup_line(user_id, gender="male"):
    """
    Generates a random pickup line based on the selected gender.

    Args:
        user_id (str): Unique identifier for the user.
        gender (str): The gender ('male' or 'female') to personalize the pickup line.

    Returns:
        str: A unique pickup line based on the selected gender.
    """
    # Store or update the user's gender
    user_genders[user_id] = gender

    # Load and update the template with the gender
    template = load_template(gender)
    
    # Create the prompt from the template
    prompt = ChatPromptTemplate.from_template(template)
    
    # Chain the prompt with the model
    chain = prompt | model
    
    # Invoke the model to generate the pickup line
    result = chain.invoke({})
    
    # Return the generated result (remove leading/trailing spaces)
    return result.strip()
