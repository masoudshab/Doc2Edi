import os
from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential
import json


def extract_data_from_pdf(pdf_path):
    # Configure Azure Form Recognizer client
    endpoint = "https://<project-name>.cognitiveservices.azure.com/"
    key = "<azure-key>"
    credential = AzureKeyCredential(key)
    form_recognizer_client = FormRecognizerClient(endpoint, credential)

    # Read the PDF file
    with open(pdf_path, "rb") as file:
        form = file.read()

    # Start the Form Recognizer job
    poller = form_recognizer_client.begin_recognize_content(form)
    result = poller.result()

    # Extract the recognized content
    data = {}
    for page in result:
        for line in page.lines:
            if line.text:
                data[line.text] = line.bounding_box

    return data

# Usage example
file_name = "DELIVERY COVER NOTE"
pdf_path = "<file-path>" + file_name + ".pdf"
json_path = "<file-path>" + file_name.replace(" ", "_") + ".json"
data = extract_data_from_pdf(pdf_path)

# Write the dictionary to the JSON file
with open(json_path, "w") as json_file:
    json.dump(data, json_file)

print("Dictionary successfully written to JSON file.")

