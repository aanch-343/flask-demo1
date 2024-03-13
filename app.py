
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
from PIL import Image
import io
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get the root directory of the Flask app
root_dir = os.path.dirname(os.path.abspath(__file__))

@app.route('/receive-image', methods=['POST'])
def receive_image():
    try:
        # Extract image buffer, image name, question, and answer key from request body
        image_data = request.json['image']
        image_name = request.json['imageName']
        question = request.json['question']
        answer_key = request.json['answerkey']

        # Convert image buffer to image
        image = Image.open(io.BytesIO(bytearray(image_data)))

        # Save the image in the root directory
        image_path = os.path.join(root_dir, image_name + '.jpg')
        image.save(image_path)

        # Print basic information about the received image
        print("Image saved at:", image_path)
        print("Image Name:", image_name)
        print("Image Format:", image.format)
        print("Image Mode:", image.mode)
        print("Image Size:", image.size)

        # Return a response acknowledging the receipt of data along with the question and answer key
        return jsonify(message="Data received and image saved", question=question, answer_key=answer_key), 200
    except Exception as e:
        print("Error receiving data:", str(e))
        return jsonify(error="Error receiving data"), 500

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app

