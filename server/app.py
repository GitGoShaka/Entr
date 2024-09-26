from flask_cors import CORS
from server import create_app
from flask import Flask, request, jsonify
import os
import openai
import pdfplumber


app = create_app()
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def read_pdf(file_name):
    """Extracts text from the given PDF file."""
    with pdfplumber.open(file_name) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

def gen_prompt(text):
    """Generates a structured JSON format of the invoice using OpenAI API."""
    prompt = f"""
    You are an intelligent assistant. Read the following invoice and output its details in a structured JSON format. The JSON should include:
    - Invoice number
    - Date
    - Bill to (name and address)
    - Ship to (if available)
    - Items (with quantity, description, unit price, total price)
    - Subtotal, Tax, and Total Amount

    Invoice Text:
    {text}

    Output the structured invoice in the following JSON format:
    {{
        "invoice_number": "",
        "date": "",
        "bill_to": {{
            "name": "",
            "address": ""
        }},
        "ship_to": {{
            "name": "",
            "address": ""
        }},
        "items": [
            {{
                "quantity": "",
                "description": "",
                "unit_price": "",
                "total_price": ""
            }}
        ],
        "subtotal": "",
        "tax": "",
        "total_amount": ""
    }}
    """
    return prompt


@app.route('/api/home')
def home():
    return jsonify({"message": "Hello from Flask!"})

@app.route('/api/upload-pdf', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['pdf']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and file.filename.endswith('.pdf'):
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)
        return jsonify({"message": "File uploaded successfully"}), 200
    else:
        return jsonify({"error": "Invalid file type"}), 400

if __name__ ==  '__main__':
    app.run(port=8080, debug=True)

@app.route('/api/process-pdf', methods=['POST'])
def process_pdf():
    data = request.json
    file_name = data.get('file_name')
    
    if not file_name:
        return jsonify({"error": "No file name provided"}), 400
    
    pdf_path = os.path.join(UPLOAD_FOLDER, file_name)
    
    if not os.path.exists(pdf_path):
        return jsonify({"error": "File not found"}), 404
    
    try:
        pdf_text = read_pdf(pdf_path)
        prompt = gen_prompt(pdf_text)
        
        print(prompt)
        
        client = openai.OpenAI(api_key=app.config['OPENAI_API_KEY'])
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=1500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        
        print(response)
        
        analysis = response.choices[0].message.content
        
        return jsonify(analysis), 200
    
    except Exception as e:
        return jsonify(str(e)), 500

