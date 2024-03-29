from flask import Flask, request, jsonify
from flask_cors import CORS
from max_sim import combined_similarity

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Dictionary to store maximum marks for each question
max_marks = {
    '1': 9,
    '2': 8,
    '3': 9,
    '4': 8,
    '5': 8,
    '6': 8,
    '7': 8,
    '8': 8,
    '9': 9,
    '10': 8,
    '11': 9,
    '12': 8
}

@app.route('/receive-image', methods=['POST'])
def receive_image():
    try:
        # Extract data from the request body
        request_data = request.json
        answer_key_data = request_data['requestData']
        usn = request_data['usn']

        # Initialize a dictionary to store similarity scores for each answer
        similarity_scores = {}

        # Iterate over the answer key data
        for question_key, answer_key in answer_key_data.items():
            if question_key.startswith('answerkey'):
                # Extract question number
                question_number = question_key[len('answerkey'):]

                # Construct the key to retrieve the answer sheet
                answer_sheet_key = 'answersheet' + question_number

                print("Question Number:", question_number)
                print("Answer Key:", answer_key)
                answer_sheet = answer_key_data.get(answer_sheet_key)
                print("Answer Sheet:", answer_sheet)

                if answer_sheet:
                    # Calculate similarity using the combined_similarity function
                    contextual_similarity, synonym_similarity = combined_similarity(answer_sheet, answer_key)

                    # Scale the similarities based on maximum marks
                    max_mark = max_marks.get(question_number, 10)  # Default to 10 if max mark not found
                    contextual_scaled = round((contextual_similarity * max_mark))
                    synonym_scaled = round((synonym_similarity * max_mark))

                    # Choose the maximum scaled similarity
                    max_similarity = max(contextual_scaled, synonym_scaled)

                    # Store the max similarity for this question
                    similarity_scores[question_number] = max_similarity

        # Print the response for cross-checking
        response = {
            "message": "Similarity scores calculated successfully",
            "usn": usn,
            "similarity_scores": similarity_scores
        }
        print("Response:", response)

        # Return the calculated similarity scores and the USN to the client
        return jsonify(response), 200

    except Exception as e:
        print("Error processing data:", str(e))
        return jsonify(error="Error processing data"), 500

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app
