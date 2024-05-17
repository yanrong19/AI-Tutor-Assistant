from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('mainchat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    # Here you can add logic for the chatbot response
    bot_response = f"Bot says: {user_message}"
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
