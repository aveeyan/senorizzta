import cv2
from PIL import Image
import pytesseract

def preprocess_image(image_path):
    # Read the image using OpenCV
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    
    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to make text more distinct
    _, thresh_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)
    
    # Save the preprocessed image temporarily
    preprocessed_path = "preprocessed_image.png"
    cv2.imwrite(preprocessed_path, thresh_image)
    return preprocessed_path

def extract_text_from_image(image_path):
    try:
        # Preprocess the image
        preprocessed_path = preprocess_image(image_path)
        
        # Open the preprocessed image with PIL
        image = Image.open(preprocessed_path)
        
        # Extract text using pytesseract
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error: {e}")
        return None

# Usage
image_file = "./scripts/test_chat.png"
extracted_text = extract_text_from_image(image_file)

print("Extracted Text:")
print(extracted_text)
