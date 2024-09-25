from flask import render_template, request, Blueprint, redirect, flash, url_for, current_app
from webApp import db
from webApp.models import Entry
from webApp.main.forms import PDFUploadForm
import os
import openai
import base64
import pdfplumber

main = Blueprint('main', __name__)



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




@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
def home():
    form = PDFUploadForm()
    if form.validate_on_submit():
        if form.pdf_file.data:
            pdf_file = form.pdf_file.data
            pdf_path = os.path.join(current_app.root_path, 'invoices', pdf_file.filename)
            pdf_file.save(pdf_path)
            pdf_text = read_pdf(pdf_path)
            prompt = gen_prompt(pdf_text)

            print(prompt)

            
            # Upload the PDF file to OpenAI
            client = openai.OpenAI(api_key=current_app.config['OPENAI_API_KEY'])

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

            # Pass the response to the template
            return render_template('index.html', title='Entr', form=form, analysis=analysis)
            

            flash('Your invoice has been uploaded and processed!', 'success')
            return redirect(url_for('main.home'))

    return render_template('index.html', title='Entr', form=form)

@main.route("/entry/new", methods=['GET', 'POST'])
def new_entry():
    form = EntryForm()

    if form.validate_on_submit():
        entry = Entry(title=form.title.data, description=form.description.data)
        db.session.add(entry)
        db.session.commit()
        flash('Your entry has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_entry.html', title='New Entry',
                           form=form)

@main.route("/entry/<int:entry_id>/delete", methods=['POST'])
def delete_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    flash('Your entry has been deleted!', 'success')
    return redirect(url_for('main.home'))

@main.route("/about")
def about():
    return render_template('about.html', title='About')




