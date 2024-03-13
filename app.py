
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
import os
import shutil

app = Flask(__name__)

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

            # Get the directory where this script is located
            script_dir = os.path.dirname(__file__)

            # Save the image in the same directory as this script
            image_path = os.path.join(script_dir, image_name + '.jpg')

            # Open a new file and write the image data to it
            with open(image_path, 'wb') as f:
                f.write(image_bytes)

            # Log the received data
            print("Image:", image_name)
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

