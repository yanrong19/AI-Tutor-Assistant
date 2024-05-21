from flask import Flask, render_template, request, jsonify
import os
from utils.function import create_vectorstore

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

# Initialise vectorstore
db = None

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def home():
    return render_template('mainchat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    
    global db
    if db:
        bot_response = f"AI Tutor: db has been ingested"
    else:
        bot_response = f"AI Tutor: db has not been ingested"
    return jsonify({'response': bot_response})

@app.route('/files', methods=['GET'])
def get_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify({'files': files})

@app.route('/ingestfiles', methods=['GET'])
def ingest_files():
    global db
    db = create_vectorstore()
    return jsonify({'message': 'Ingestion completed'})

@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist('files')
    for file in files:
        if file.filename != '':
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return jsonify({'success': 'Files uploaded successfully'}), 200

@app.route('/delete-file', methods=['POST'])
def delete_file():
    filename = request.json['filename']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'success': f'{filename} deleted successfully'}), 200
    else:
        return jsonify({'error': f'{filename} not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
