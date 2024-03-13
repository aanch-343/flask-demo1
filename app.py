
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
from flask import Flask, request, jsonify
from flask_cors import CORS
from pytesseract import image_to_string
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def process_image(image_data):
    # Convert base64 encoded image data to numpy array
    nparr = np.fromstring(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Preprocessing:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  # Thresholding

    # Perform OCR on the preprocessed image
    text = image_to_string(thresh, lang='eng', config='--psm 6')

    return text

@app.route('/receive-image', methods=['POST'])
def receive_image():
    try:
        # Extract image buffer, image name, question, and answer key from request body
        image_data = request.json['image']
        image_name = request.json['imageName']
        question = request.json['question']
        answer_key = request.json['answerkey']

        # Process the received image to extract text
        extracted_text = process_image(image_data)

        # Log the received data and extracted text
        print("Image:", image_name)
        print("Question:", question)
        print("Answer Key:", answer_key)
        print("Image Buffer:", image_data)
        print("Extracted Text:", extracted_text)

        # Return a response acknowledging the receipt of data along with the question, answer key, and extracted text
        response_data = {
            "message": "Data received and logged",
            "question": question,
            "answer_key": answer_key,
            "extracted_text": extracted_text
        }
        return jsonify(response_data), 200
    except Exception as e:
        print("Error receiving or processing data:", str(e))
        return jsonify(error="Error receiving or processing data"), 500

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app
