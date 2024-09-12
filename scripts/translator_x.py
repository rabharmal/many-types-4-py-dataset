import argparse
import json
import os
from pathlib import Path

def parse_type_prediction(pred):
    # Ensuring that the prediction is parsed correctly and returns a string instead of a list
    if pred:
        return pred if isinstance(pred, str) else pred[0] if isinstance(pred, list) and pred else "Unknown"
    return "Unknown"
    
def remove_duplicates(entries):
    unique_entries = []
    seen = set()
    for entry in entries:
        identifier = json.dumps(entry, sort_keys=True)  # Use JSON string as the unique identifier
        if identifier not in seen:
            seen.add(identifier)
            unique_entries.append(entry)
    return unique_entries

def translate_content(data):
    if not data:
        return []

    if isinstance(data, list):
        translated_output = []
        for item in data:
            translated_output.extend(process_translation(item))
        return remove_duplicates(translated_output)
    else:
        return remove_duplicates(process_translation(data))

def process_translation(data):
    output = []
    print(f"Data Type Check: {type(data)}")  # Should be 'dict'

     # Loop through each project
    for project_name, project_data in data.items():
        src_files = project_data.get('src_files', {})

        # Loop through each file in the source files
        for file_path, file_data in src_files.items():
            file_name = Path(file_path).name

            # Here, file_data is actually the dictionary with file details as you described
            # We can process classes and functions directly here
            all_functions = file_data.get('funcs', [])
            for cls in file_data.get('classes', []):
                # print("Class: ", cls)
                all_functions.extend(cls.get('funcs', []))

            for func in all_functions:
                process_function(output, func, file_name, project_name)

    return output

def process_function(output, func, file_name, project_name):
    name = func["name"]
    fn_lc = func["fn_lc"]

    # Adding correct parsing for the function type and parameters
    function_entry = {
        "project_name": project_name,
        "file": file_name,
        "line_number": fn_lc[0][0],
        "function": name,
        "type": parse_type_prediction(func.get("ret_type")),
        "all_type_preds": func.get("ret_type", "Unknown"),
    }
    output.append(function_entry)

    # Parsing and adding function parameters
    for param, param_type in func.get("params", {}).items():
        output.append({
            "project_name": project_name,
            "file": file_name,
            "line_number": fn_lc[0][0],
            "parameter": param,
            "function": name,
            "type": parse_type_prediction(param_type),
            "all_type_preds": param_type or "Unknown"
        })

    # Parsing and adding function variables
    for var, var_type in func.get("variables", {}).items():
        var_lns = func.get("fn_var_ln", {}).get(var, [])
        for var_ln in var_lns:
            output.append({
                "project_name": project_name,
                "file": file_name,
                "line_number": var_ln[0],
                "variable": var,
                "function": name,
                "type": parse_type_prediction(var_type),
                "all_type_preds": var_type or "Unknown"                
            })

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--json_file", help="Path to the output.json file", required=True, default="output.json")
    # parser.add_argument("--output_file", help="Path to save the translated content", default="translated_output.json")

    # args = parser.parse_args()

    # json_file_path = args.json_file
    # if not os.path.exists(json_file_path):
    #     print(f"Error: The file {json_file_path} does not exist.")
    #     exit(1)

    # with open(json_file_path, 'r') as f:
    #     data = json.load(f)

    # translated_content = translate_content(data)

    # output_file_path = args.output_file
    # with open(output_file_path, 'w') as f:
    #     json.dump(translated_content, f, indent=4)

    # print(f"Translated content saved to {output_file_path}")
    pass