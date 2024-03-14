from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/receive-image', methods=['POST'])
def receive_image():
    try:
        # Extract image buffer, image name, question, and answer key from request body
        image_data = request.json['image']
        # image_name = request.json['imageName']
        question = request.json['question']
        answer_key = request.json['answerkey']

        # Log the received data
        # print("Image:", image_name)
        print("Question:", question)
        print("Answer Key:", answer_key)
        print("Image :", image_data)

        # Return a response acknowledging the receipt of data along with the question and answer key
        return jsonify(message="Data received and logged", question=question, answer_key=answer_key,image_data=image_data), 200
    except Exception as e:
        print("Error receiving data:", str(e))
        return jsonify(error="Error receiving data"), 500

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app
