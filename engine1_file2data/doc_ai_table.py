# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# [START documentai_process_ocr_document]

# TODO(developer): Uncomment these variables before running the sample.
# project_id= 'oko1-385920'
# location = 'ualberta.ca' # Format is 'us' or 'eu'
# processor_id = 'b883d78b09cd9bdf' # Create processor in Cloud Console
# file_path = 'C:\Users\Shahed\OneDrive\Documents\DO905.pdf'

import argparse
from typing import Sequence

from google.api_core.client_options import ClientOptions
from google.cloud import documentai
from typing import List, Sequence
import pandas as pd
import os
import json

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--pdf", required=False,help="path to input PDF File be OCR'd")
ap.add_argument("-f", "--folder", required=False,help="folder path for output csv and json files")
args = vars(ap.parse_args())

folder = args["folder"]
file_path = args["pdf"]

# project_id= 'ocr-anirbankonar123'
# location = 'us'
# processor_id = 'c808e3e8c59b5540'
# project_id= 'oko1-385920'
# location = 'ualberta.ca' # Format is 'us' or 'eu'
# processor_id = 'b883d78b09cd9bdf' # Create processor in Cloud Console

project_id= 'oko2-386015'
location = 'us' # Format is 'us' or 'eu'
processor_id = 'f29e90f280aa04e0' # Create processor in Cloud Console
file_path = r'C:\Users\Shahed\OneDrive\Documents\HAWB3441084.pdf'
mime_type = 'application/pdf'

def get_table_data(
    rows: Sequence[documentai.Document.Page.Table.TableRow], text: str
) -> List[List[str]]:
    """
    Get Text data from table rows
    """
    all_values: List[List[str]] = []
    for row in rows:
        current_row_values: List[str] = []
        for cell in row.cells:
            current_row_values.append(
                text_anchor_to_text(cell.layout.text_anchor, text)
            )
        all_values.append(current_row_values)
    return all_values

def text_anchor_to_text(text_anchor: documentai.Document.TextAnchor, text: str) -> str:
    """
    Document AI identifies table data by their offsets in the entirity of the
    document's text. This function converts offsets to a string.
    """
    response = ""
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    for segment in text_anchor.text_segments:
        start_index = int(segment.start_index)
        end_index = int(segment.end_index)
        response += text[start_index:end_index]
    return response.strip().replace("\n", " ")

def process_document_form_sample(
    project_id: str, location: str, processor_id: str, file_path: str, mime_type: str
):
    # Online processing request to Document AI
    document = process_document(
        project_id, location, processor_id, file_path, mime_type
    )

    text = document.text

    print(f"There are {len(document.pages)} page(s) in this document.")

    # Read the form fields and tables output from the processor
    i = 0
    json_dict = {}
    for page in document.pages:
        i += 1
        print(f"\n\n**** Page {page.page_number} ****")

        print(f"\nFound {len(page.tables)} table(s):")
        tab_ctr=0
        for table in page.tables:
            tab_ctr+=1
            num_collumns = len(table.header_rows[0].cells)
            num_rows = len(table.body_rows)
            print(f"Table with {num_collumns} columns and {num_rows} rows:")

            # Print header rows
            print("Columns:")
            print_table_rows(table.header_rows, text)
            # Print body rows
            print("Table body data:")
            print_table_rows(table.body_rows, text)


            header_row_values: List[List[str]] = []
            body_row_values: List[List[str]] = []

            header_row_values = get_table_data(table.header_rows, document.text)
            body_row_values = get_table_data(table.body_rows, document.text)

            df = pd.DataFrame(
                data=body_row_values,
                columns=pd.MultiIndex.from_arrays(header_row_values),
            )

            df.to_csv(folder+"/page"+str(i)+"_"+str(tab_ctr)+".csv")
            print(f"\nFound {len(page.form_fields)} form field(s):")


        for field in page.form_fields:
            name = layout_to_text(field.field_name, text)
            value = layout_to_text(field.field_value, text)
            print(f"    * {repr(name.strip())}: {repr(value.strip())}")

        if(i==1):
            for field in page.form_fields:
                name = layout_to_text(field.field_name, text)
                value = layout_to_text(field.field_value, text)
                json_dict[name.strip()]=value.strip()
                print(f"    * {repr(name.strip())}: {repr(value.strip())}")

    jsonString = json.dumps(json_dict, indent=4)

    with open(folder+"/header.json", "w") as json_file:
        json.dump(json_dict, json_file)

def process_document(
    project_id: str, location: str, processor_id: str, file_path: str, mime_type: str
) -> documentai.Document:
    # You must set the api_endpoint if you use a location other than 'us', e.g.:
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load Binary Data into Document AI RawDocument Object
    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)

    return result.document

def print_table_rows(
    table_rows: Sequence[documentai.Document.Page.Table.TableRow], text: str
) -> None:
    for table_row in table_rows:
        row_text = ""
        for cell in table_row.cells:
            cell_text = layout_to_text(cell.layout, text)
            row_text += f"{repr(cell_text.strip())} | "
        print(row_text)

def layout_to_text(layout: documentai.Document.Page.Layout, text: str) -> str:
    """
    Document AI identifies text in different parts of the document by their
    offsets in the entirety of the document's text. This function converts
    offsets to a string.
    """
    response = ""
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    for segment in layout.text_anchor.text_segments:
        start_index = int(segment.start_index)
        end_index = int(segment.end_index)
        response += text[start_index:end_index]
    return response

process_document_form_sample(project_id, location, processor_id, file_path,mime_type)

