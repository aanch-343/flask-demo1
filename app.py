
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# @app.route('/receive-image', methods=['POST'])
# def receive_image():
#     try:
#         # Extract image buffer, image name, question, and answer key from request body
#         image_data = request.json['image']
#         image_name = request.json['imageName']
#         question = request.json['question']
#         answer_key = request.json['answerkey']

#         # Log the received data
#         print("Image:", image_name)
#         print("Question:", question)
#         print("Answer Key:", answer_key)
#         print("Image Buffer:", image_data)

#         # Return a response acknowledging the receipt of data along with the question and answer key
#         return jsonify(message="Data received and logged", question=question, answer_key=answer_key), 200
#     except Exception as e:
#         print("Error receiving data:", str(e))
#         return jsonify(error="Error receiving data"), 500

# if __name__ == '_main_':
#     app.run(debug=True)  # Run the Flask app
# main.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from ocr import process_image
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/receive-image', methods=['POST'])
def receive_image():
    try:
        # Extract image data, image name, question, and answer key from request body
        image_data = base64.b64decode(request.json['image'])
        image_name = request.json['imageName']
        question = request.json['question']
        answer_key = request.json['answerkey']

        # Process the received image to extract text
        extracted_text = process_image(image_data)

        # Log the received data and extracted text
        print("Image:", image_name)
        print("Question:", question)
        print("Answer Key:", answer_key)
        print("Image Buffer Size:", len(image_data))
        print("Extracted Text:", extracted_text)

        # Return a response acknowledging the receipt of data along with the question, answer key, and extracted text
        return jsonify(message="Data received and logged", question=question, answer_key=answer_key, extracted_text=extracted_text), 200
    except Exception as e:
        print("Error receiving or processing data:", str(e))
        return jsonify(error="Error receiving or processing data"), 500

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app
