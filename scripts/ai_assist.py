from PIL import Image
import pytesseract

def extract_text_from_image(image_path):
    try:
        # Open the image using Pillow
        img = Image.open(image_path)
        
        # Use pytesseract to extract text from the image
        extracted_text = pytesseract.image_to_string(img)
        
        return extracted_text
    except Exception as e:
        return f"An error occurred: {e}"

# Replace 'your_image.png' with the path to your image file
image_path = './scripts/test_chat.png'
text = extract_text_from_image(image_path)

print("Extracted text from the image:")
print(text)
