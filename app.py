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

@app.route("/receive-image", methods=["POST"])
def receive_image():
  try:
    # Receive data from the request
    data = request.get_data()  # Access raw bytes
    image_buffer = data[: data.find(b"\r\n\r\n")]  # Extract image data

    # Extract form data (modify as needed)
    form_data = data[data.find(b"\r\n\r\n") + 4:].decode("utf-8")
    question = form_data.split("&")[0].split("=")[1]
    answerkey = form_data.split("&")[1].split("=")[1]

    # Process image and form data (replace with your logic)
    print("Received Image Buffer:", image_buffer)
    print("Question:", question)
    print("Answer Key:", answerkey)

    return jsonify({"message": "Data received successfully"}), 200
  except Exception as e:
    print("Error receiving data:", str(e))
    return jsonify({"error": "Error receiving data"}), 500

if __name__ == "_main_":
  app.run(debug=True)