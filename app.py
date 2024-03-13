
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
from PIL import Image
import io
import base64
import os

app = Flask(__name__)

@app.route('/receive-image', methods=['POST'])
def receive_image():
    try:
        # Ensure request data is in JSON format
        if request.is_json:
            # Extract JSON data from request
            request_data = request.json
            
            # Extract image data, image name, question, and answer key from request JSON
            image_data_base64 = request_data['image']
            image_name = request_data['imageName']
            question = request_data['question']
            answer_key = request_data['answerkey']

            # Decode base64-encoded image data
            image_data = base64.b64decode(image_data_base64)

            # Open image using PIL
            image = Image.open(io.BytesIO(image_data))

            # Get the directory path of the current script
            script_directory = os.path.dirname(__file__)

            # Create a directory named 'images' within the script directory if it doesn't exist
            images_directory = os.path.join(script_directory, 'images')
            if not os.path.exists(images_directory):
                os.makedirs(images_directory)

            # Save the image in the 'images' directory
            image_path = os.path.join(images_directory, image_name + '.jpg')
            image.save(image_path)

            # Log the received data
            print("Image saved at:", image_path)
            print("Question:", question)
            print("Answer Key:", answer_key)

            # Return a response acknowledging the receipt of data
            return jsonify(message="Data received and logged"), 200
        else:
            return jsonify(error="Request data is not in JSON format"), 400
    except Exception as e:
        print("Error receiving data:", str(e))
        return jsonify(error="Error receiving data"), 500

if __name__ == '__main__':
    app.run(debug=True)
