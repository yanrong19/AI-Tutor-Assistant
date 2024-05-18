from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

uploaded_files = []

@app.route('/')
def home():
    return render_template('mainchat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    # Here you can add logic for the chatbot response
    bot_response = f"Bot says: {user_message}"
    return jsonify({'response': bot_response})

@app.route('/files', methods=['GET'])
def get_files():
    return jsonify({'files': uploaded_files})

@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist('files')
    for file in files:
        if file.filename != '':
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if filename not in uploaded_files:
                uploaded_files.append(filename)
    return jsonify({'success': 'Files uploaded successfully'}), 200

@app.route('/delete-file', methods=['POST'])
def delete_file():
    filename = request.json['filename']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        if filename in uploaded_files:
            uploaded_files.remove(filename)
        return jsonify({'success': f'{filename} deleted successfully'}), 200
    else:
        return jsonify({'error': f'{filename} not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
