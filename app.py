import scripts.chat_logic as chat_logic
import scripts.rizz_me as rizz_logic
from flask import Flask, request, redirect, url_for, render_template, jsonify

app = Flask(__name__)

# Redirect "/" to "/chat"
@app.route("/")
def home():
    return redirect(url_for("page_chatbot"))

@app.route("/chat", methods=["GET", "POST"])
def page_chatbot():
    # If the request is a GET, render the chatbot page
    if request.method == "GET":
        return render_template("chatbot.html")
    
    # If it's a POST request, handle the chatbot logic
    elif request.method == "POST":
        try:
            data = request.json
            user_id = data.get("user_id", "default")  # Unique user ID (use session/cookies for real app)
            user_message = data.get("message", "")

            # Get bot response using chat_logic
            bot_response = chat_logic.handle_chat(user_id, user_message)
            return jsonify({"response": bot_response})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route("/rizzme", methods=["GET", "POST"])
def page_rizzme():
    # If the request is a GET, render the rizzme page
    if request.method == "GET":
        return render_template("rizzme.html")

    # If it's a POST request, handle the rizzme logic
    elif request.method == "POST":
        try:
            # Get the gender from the request data (default to 'male' if not provided)
            gender = request.json.get("gender", "male")
            
            # Generate a pickup line based on the gender
            pickup_line = rizz_logic.generate_pickup_line(gender)

            return jsonify({"pickup_line": pickup_line})
        except Exception as e:
            return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
