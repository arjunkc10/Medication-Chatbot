from flask import Flask, request, jsonify

app = Flask(__name__)

# Example data
symptoms_medications = {
    "fever": ["Paracetamol", "Ibuprofen"],
    "headache": ["Aspirin", "Paracetamol"],
    "cough": ["Cough syrup", "Honey and lemon"],
    # Add more scraped data here...
}

# Chatbot route
@app.route('/get_medication', methods=['POST'])
def get_medication():
    user_data = request.json
    symptoms = user_data.get("symptoms", [])
    
    # Check for medications for each symptom
    medications = []
    for symptom in symptoms:
        if symptom in symptoms_medications:
            medications.extend(symptoms_medications[symptom])
    
    if medications:
        response = {"medications": list(set(medications))}
    else:
        response = {"message": "No matching medications found. Please consult a healthcare professional."}
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
