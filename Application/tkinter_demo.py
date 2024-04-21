import json
import pandas as pd
import tkinter as tk
from tkinter import Tk, filedialog

def load_json(filename):
    """Load a JSON file."""
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def traverse_elements(elements, depth=0, path=[]):
    """Recursively traverse elements in the JSON and extract required data."""
    rows = []
    for element in elements:
        current_path = path + [element.get("idShort", "")]
        current_name = current_path[-1] if current_path else ""
        model_type = element.get("modelType", "Other")
        
        descriptions = element.get("description", [])
        desc_en = next((desc["text"] for desc in descriptions if desc["language"] == "en"), "")
        desc_kr = next((desc["text"] for desc in descriptions if desc["language"] == "kr"), "")

        semantic_id_detail = element.get("semanticId", {})
        semantic_keys = semantic_id_detail.get("keys", [])
        semantic_id = next((key["value"] for key in semantic_keys if key.get("value")), "")

        # Append current element information
        rows.append([" > ".join(current_path), model_type, current_name, semantic_id, "", desc_en, desc_kr])
        
        # Process nested submodel elements if they exist
        if "value" in element and isinstance(element["value"], list):
            rows.extend(traverse_elements(element["value"], depth + 1, current_path))
        elif "submodelElements" in element:
            rows.extend(traverse_elements(element["submodelElements"], depth + 1, current_path))

    return rows

def save_to_excel(data, output_file):
    """Save the data to an Excel file."""
    df = pd.DataFrame(data, columns=["Data Depth", "Type", "Name", "Semantic ID", "New Semantic ID", "Description (EN)", "Description (KR)"])
    df.to_excel(output_file, index=False)

def main():
    """Main function to load JSON, process data, and save to Excel."""
    root = Tk()
    root.title("json to exel program")
    root.withdraw()  # Hide the main window

    print("json to exel program")


    filename = filedialog.askopenfilename(title="Select a JSON file", filetypes=[("JSON files", "*.json")])
    if not filename:
        print("파일이 아닙니다.")
        return
    
    data = load_json(filename)
    extracted_data = traverse_elements(data['submodelElements'])
    output_file = filedialog.asksaveasfilename(title="Save as", filetypes=[("Excel files", "*.xlsx")], defaultextension=".xlsx")
    if output_file:
        save_to_excel(extracted_data,output_file)
    
    print("Program Closed")

if __name__ == "__main__":
    main()