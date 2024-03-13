
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
import base64
import io
import pytesseract
from PIL import Image
import cv2

app = Flask(__name__)

def image_to_text(image_file):
    img = cv2.imread(image_file)

    # Preprocessing:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  # Thresholding

    # Optional deskewing (if needed):
    # deskewed = deskew(thresh)

    text = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')  # Use the preprocessed image

    return text

@app.route('/receive-image', methods=['POST'])
def receive_image():
    try:
        # Ensure request data is in JSON format
        if request.is_json:
            # Extract JSON data from request
            request_data = request.json
            
            # Extract image data, image name, question, and answer key from request JSON
            image_data_base64 = request_data.get('image')
            image_name = request_data.get('imageName')
            question = request_data.get('question')
            answer_key = request_data.get('answerkey')

            if not all([image_data_base64, image_name, question, answer_key]):
                return jsonify(error="Missing required fields"), 400

            # Decode base64-encoded image data
            image_bytes = base64.b64decode(image_data_base64.encode('utf-8'))

            # Convert image buffer to PIL Image
            image = Image.open(io.BytesIO(image_bytes))

            # Save the image to a temporary file
            temp_image_path = 'temp_image.png'
            image.save(temp_image_path)

            # Perform OCR on the image
            ocr_text = image_to_text(temp_image_path)

            # Log the received data and OCR text
            print("Image:", image_name)
            print("Question:", question)
            print("Answer Key:", answer_key)
            print("OCR Text:", ocr_text)

            # Delete the temporary image file
            os.remove(temp_image_path)

            # Return the OCR text as a response
            return jsonify(message="OCR completed", ocr_text=ocr_text), 200
        else:
            return jsonify(error="Request data is not in JSON format"), 400
    except Exception as e:
        print("Error receiving or processing data:", str(e))
        return jsonify(error="Error receiving or processing data"), 500

if __name__ == '__main__':
    app.run(debug=True)
