# Doc2Edi

![alt text](https://github.com/[username]/[reponame]/blob/[branch]/image.jpg?raw=true)

## First Engine: 
## Extracting Data from Document PDF Files Using GCP and Google Document AI

### Steps for Engine-1  
1- create new project on GCloud: https://codelabs.developers.google.com/codelabs/docai-ocr-python#1
2- create service account for this project: https://console.cloud.google.com/iam-admin/iam?walkthrough_id=iam--create-service-account&project=oko2-386015

NOTE: these roles should be selected for this service account: Document AI Administrator
Document AI API User

3- create a processor for my project: https://cloud.google.com/document-ai/docs/create-processor?_ga=2.114028359.-1141760794.1683471749
NOTE: for this project I used Form Parser from G Doc AI

4- cloned this repo:  https://github.com/anirbankonar123/documentai 
5- added my auth key location into my windows env variables as: GOOGLE_APPLICATION_CREDENTIALS=’path to json file’
6- copied my project and processor info into my local code
7- for each PDf file, the code ran and created one json file and multiple CSV files.

python doc_ai_table.py --pdf <pdf_path> --folder <output_path>

## Second Engine: 
## Converting Data into EDI 211 Transmission Files

### Steps for Engine-2  


1- required fields for EDI 211:
• Shipment ID number
• Date and time (of pick-up / delivery)
• Status report request (upon delivery)
• Business instructions
• Handling requirements
• Bill of lading rates and charges
• Lading quantity / weight / freight Class / value
• Contact information



# Resources:
1) Google Cloud solution:
2) Document AI tutorial
3) How to setup my Doc AI project: https://codelabs.developers.google.com/codelabs/docai-ocr-python#0 
