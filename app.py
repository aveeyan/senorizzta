from flask import Flask, request, redirect, url_for, render_template, jsonify
import logging
from scripts.chat_logic import Chatbot
from scripts.rizz_logic import generate_pickup_line

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

@app.route("/assist", methods=["GET", "POST"])
def page_assist():
    return render_template("assist.html")

if __name__ == "__main__":
    app.run(debug=True)