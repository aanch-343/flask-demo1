# from flask import Flask, request, jsonify
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# @app.route('/receive-image', methods=['GET', 'POST'])
# def receive_image():
#     try:
#         # Receive data from the request
#         image_buffer = request.get_data()
#         image_name = request.form['imageName']
#         question = request.form['question']
#         answer_key = request.form['answerkey']

#         # Log received data
#         print("Received Image Buffer:", image_buffer)
#         print("Image Name:", image_name)
#         print("Question:", question)
#         print("Answer Key:", answer_key)

#         # Respond with success message
#         return jsonify({"message": "Data received successfully"}), 200
#     except Exception as e:
#         print("Error receiving data:", str(e))
#         return jsonify({"error": "Error receiving data"}), 500

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/receive-image', methods=['POST'])
def receive_image():
    try:
        # Extract image buffer, image name, question, and answer key from request body
        image_data = request.json['image']
        image_name = request.json['imageName']
        question = request.json['question']
        answer_key = request.json['answerkey']

        # Log the received data
        print("Image:", image_name)
        print("Question:", question)
        print("Answer Key:", answer_key)
        print("Image Buffer:", image_data)

        print("Data received and logged successfully")
        return jsonify(message="Data received and logged"), 200
    except Exception as e:
        print("Error receiving data:", str(e))
        return jsonify(error="Error receiving data"), 500

if __name__ == '_main_':
    app.run(debug=True)  # Run the Flask app