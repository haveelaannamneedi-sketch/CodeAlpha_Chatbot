
from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Simple Chatbot</title>
    <style>
        body {
            font-family: Arial;
            background: #f0eaff;
            text-align: center;
            padding: 40px;
        }
        .chatbox {
            background: white;
            max-width: 500px;
            margin: auto;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 12px #ccc;
        }
        input {
            padding: 12px;
            width: 65%;
            border-radius: 8px;
            border: 1px solid #aaa;
        }
        button {
            padding: 12px;
            background: #7048e8;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }
        .reply {
            background: #eee8ff;
            padding: 15px;
            margin-top: 20px;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <div class="chatbox">
        <h1>🤖 Simple Chatbot</h1>
        <p>Ask me something!</p>

        <form method="POST">
            <input type="text" name="message"
                   placeholder="Type your message..." required>
            <button type="submit">Send</button>
        </form>

        {% if reply %}
            <div class="reply">
                <b>Bot:</b> {{ reply }}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""


def get_reply(message):
    from difflib import SequenceMatcher

    user_message = message.lower().strip()

    knowledge_base = [
        ("hello", "Hello! How can I help you?"),
        ("hi", "Hello! How can I help you?"),
        ("good morning", "Good morning! 😊 How can I help you?"),
        ("what is your name", "I am your Simple Chatbot."),
        ("who are you", "I am your Simple Chatbot."),
        ("how are you", "I am fine! Thank you."),
        ("what can you do", "I can answer questions from my knowledge base."),
        ("what is cloud computing", "Cloud computing provides computing services over the internet."),
        ("thank you", "You're welcome! Happy to help."),
        ("help", "You can ask me about Python, cloud computing, or my features."),
        ("what is python", "Python is a popular programming language."),
        ("tell me about python", "Python is a popular programming language."),
        ("bye", "Goodbye! Have a nice day!"),
    ]

    best_answer = None
    best_score = 0

    for question, answer in knowledge_base:
        if question in user_message:
            return answer

        score = SequenceMatcher(
            None, user_message, question
        ).ratio()

        if score > best_score:
            best_score = score
            best_answer = answer

    if best_score >= 0.55:
        return best_answer

    return "Sorry, I couldn't find a matching answer. Try asking about Python, my name, or say hello."


@app.route("/", methods=["GET", "POST"])
def home():
    reply = ""

    if request.method == "POST":
        message = request.form.get("message", "")
        reply = get_reply(message)

    return render_template_string(HTML, reply=reply)

if __name__ == "__main__":
    app.run(debug=True)
