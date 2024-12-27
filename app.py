from flask import Flask, request, redirect, url_for, render_template, jsonify
import logging
from scripts.chat_logic import Chatbot
from scripts.rizz_logic import generate_pickup_line
from scripts.ai_assist import ImageTextExtractor, Assistbot

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route("/")
def home():
    return redirect(url_for("page_chatbot"))

@app.route("/chat", methods=["GET", "POST"])
def page_chatbot():
    if request.method == "POST":
        data = request.get_json()
        logging.debug(f"Received data: {data}")

        if not isinstance(data, dict):
            logging.error(f"Invalid data type received: {type(data)}")
            return jsonify({"error": "Invalid input format."}), 400

        if not data:
            return jsonify({"error": "No JSON data received."}), 400

        user_id = data.get("user_id")
        user_input = data.get("message")
        gender = data.get("gender")

        missing_params = []
        if not user_id:
            missing_params.append("user_id")
        if not user_input:
            missing_params.append("message")
        if not gender:
            missing_params.append("gender")

        if missing_params:
            missing_params_str = ", ".join(missing_params)
            logging.debug(f"Missing parameters: {missing_params_str}")
            return jsonify({"error": f"Missing required parameters: {missing_params_str}"}), 400

        # Initialize the Chatbot with user_id and gender
        chatbot = Chatbot(user_id=user_id, gender=gender)

        try:
            # Call handle_chat and handle potential errors
            response = chatbot.handle_chat(user_input)["response"]

            # Ensure the response from handle_chat is in a proper format for JSON
            if isinstance(response, str):
                return jsonify({"response": response})
            else:
                return jsonify({"error": f"Unexpected response format from handle_chat.\nResponse: {response}"}), 500
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return jsonify({"error": "An unexpected error occurred."}), 500

    return render_template("chatbot.html")

@app.route("/rizzme", methods=["GET", "POST"])
def page_rizzme():
    if request.method == "POST":
        gender = request.form.get("gender", "male")

        pickup_line = generate_pickup_line(gender)
        return jsonify({"pickup_line": pickup_line})

    return render_template("rizzme.html")

import tempfile
import cv2
@app.route("/assist", methods=["GET", "POST"])
def page_assist():
    logging.debug(f"Request method: {request.method}")
    
    if request.method == "POST":
        # Check if image file is uploaded
        if 'file' in request.files:  
            # Handle image file processing
            image_file = request.files['file']
            if image_file.filename == '':
                return jsonify({"error": "No image file provided."}), 400
            
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                image_file.save(temp_file.name)
                image = cv2.imread(temp_file.name)

            if image is None:
                logging.error("Image failed to load.")
                return jsonify({"error": "Failed to load image."}), 400
            
            try:
                text_extractor = ImageTextExtractor()
                extracted_text = text_extractor.extract_text(temp_file.name)
                logging.debug(f"Extracted text: {extracted_text}")
            except Exception as e:
                logging.error(f"Text extraction failed: {e}")
                return jsonify({"error": "Failed to extract text from the image."}), 500

            if not extracted_text.strip():
                logging.error("No text extracted from the image.")
                return jsonify({"error": "Failed to extract text from the image."}), 400
            
            try:
                assistbot = Assistbot(user_id="image_user", gender="neutral")
                response = assistbot.handle_chat(extracted_text)["response"]
                logging.debug(f"Assistbot response: {response}")
                
                if isinstance(response, (str, dict)):
                    return jsonify({"response": response})
                else:
                    logging.error(f"Unexpected response format: {type(response)}")
                    return jsonify({"error": "Unexpected response format from Assistbot."}), 500

            except Exception as e:
                logging.error(f"Assistbot interaction failed: {e}")
                return jsonify({"error": "Failed to interact with Assistbot."}), 500

        # Check if text input is provided (in request.form or JSON payload)
        elif 'text' in request.form or request.is_json:
            # Handle text input
            if request.is_json:
                data = request.get_json()
                user_input = data.get("text")
            else:
                user_input = request.form.get("text")
            
            logging.debug(f"Received text input: {user_input}")

            if not user_input or not user_input.strip():
                logging.error("No valid text input found.")
                return jsonify({"error": "No valid text input provided."}), 400

            try:
                assistbot = Assistbot(user_id="text_user", gender="neutral")
                response = assistbot.handle_chat(user_input)["response"]
                logging.debug(f"Assistbot response: {response}")
                
                if isinstance(response, (str, dict)):
                    return jsonify({"response": response})
                else:
                    logging.error(f"Unexpected response format: {type(response)}")
                    return jsonify({"error": "Unexpected response format from Assistbot."}), 500

            except Exception as e:
                logging.error(f"Assistbot interaction failed: {e}")
                return jsonify({"error": "Failed to interact with Assistbot."}), 500

        else:
            logging.error("No valid input found.")
            return jsonify({"error": "No valid input found."}), 400

    # Handle GET requests
    if "application/json" in request.headers.get("Accept", ""):
        return jsonify({"message": "Use POST to upload an image or send text."}), 400
    return render_template("assist.html")

if __name__ == "__main__":
    app.run(debug=True)