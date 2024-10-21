from pathlib import Path
import re

def parse_type_prediction(pred):
    if pred:
        return [pred] if isinstance(pred, str) else pred if isinstance(pred, list) else ["Unknown"]
    return ["Unknown"]

def remove_duplicates(entries):
    unique_entries = []
    seen = set()

    # Iterate over the entries to remove duplicates
    for entry in entries:
        # Create a unique identifier ignoring col_offset for variable/function/parameter
        if "parameter" in entry:
            identifier = (
                entry.get("file"),
                entry.get("line_number"),
                entry.get("parameter"),
                entry.get("function"),
            )
        elif "variable" in entry:
            identifier = (
                entry.get("file"),
                entry.get("line_number"),
                entry.get("variable"),
            )
        else:
            identifier = (
                entry.get("file"),
                entry.get("line_number"),
                entry.get("function"),
            )

        # Only add entry if its identifier is not already in the seen set
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
    for project_name, project_data in data.items():
        src_files = project_data.get('src_files', {})
        for file_path, file_data in src_files.items():
            full_file_path = file_path
            process_global_variables(output, file_data, full_file_path, project_name)

            all_functions = file_data.get('funcs', [])
            for cls in file_data.get('classes', []):
                process_class_variables(output, cls, full_file_path, project_name)
                all_functions.extend(cls.get('funcs', []))

            for func in all_functions:
                process_function(output, func, full_file_path, project_name)

    return output

# def process_global_variables(output, file_data, file_name, project_name):

#     global_variables = file_data.get('variables', {})
#     global_var_lines = file_data.get('mod_var_ln', {})

#     for original_var, var_type in global_variables.items():
#         var_lines = global_var_lines.get(original_var, [])
#         if "Unknown" in parse_type_prediction(var_type):
#             continue  # Skip this entry if the type is unknown
#         if var_lines:
#             for var_line in var_lines:
#                 output.append({
#                     "file": file_name,
#                     "line_number": var_line[0],
#                     "col_offset": var_line[1],
#                     "variable": original_var,
#                     "type": parse_type_prediction(var_type)                    
#                 })      

def normalize_string(s):
    """Normalize the string by removing non-alphanumeric characters and converting to lowercase."""
    return re.sub(r'[^a-zA-Z0-9]', '', s).lower()

def process_global_variables(output, file_data, file_name, project_name):
    global_variables = file_data.get('variables', {})
    global_var_lines = file_data.get('mod_var_ln', {})

    # Create a normalized version of global_var_lines for comparison
    # normalized_global_var_lines = {normalize_string(var): lines for var, lines in global_var_lines.items()}

    for var, var_type in global_variables.items():
       
        if "Unknown" in parse_type_prediction(var_type):
            continue  # Skip this entry if the type is unknown   

        if " " in var:
            var = var.replace(" ", "_")

        var_lines = global_var_lines.get(var, [])  # Compare normalized variable names
        if var_lines:
            for var_line in var_lines:
                output.append({
                    "file": file_name,
                    "line_number": var_line[0],
                    "col_offset": var_line[1],
                    "variable": var,  # Keep the original variable name for output
                    "type": parse_type_prediction(var_type)
                })

def process_class_variables(output, cls, file_name, project_name):
    class_name = cls.get('name')
    class_variables = cls.get('variables', {})
    class_var_lines = cls.get('cls_var_ln', {})

    if len(cls['variables']) != len(cls['cls_var_ln']):
        print(f"Warning: Mismatch in number of variables and variable lines for class {class_name} in {file_name}")

    for var, var_type in class_variables.items():
        if "Unknown" in parse_type_prediction(var_type):
            continue  # Skip this entry if the type is unknown

        if " " in var:
            print(f"Warning: Variable name '{var}' contains a space in class {class_name} in {file_name}")
            var = var.replace(" ", "_")  # Replace spaces with underscores

        var_lines = class_var_lines.get(var, [])
        for var_line in var_lines:
            output.append({                
                "file": file_name,
                "line_number": var_line[0],
                "col_offset": var_line[1],
                "variable": f"{class_name}.{var}",
                "type": parse_type_prediction(var_type)
            })

def process_function(output, func, file_name, project_name):
    name = func["q_name"]
    fn_lc = func["fn_lc"]

    function_type = parse_type_prediction(func.get("ret_type"))
    if "Unknown" in function_type:
        return  # Skip this function if the return type is unknown

    function_entry = {
        "file": file_name,
        "line_number": fn_lc[0][0],
        "col_offset": fn_lc[0][1],
        "function": name,
        "type": function_type,
    }
    output.append(function_entry)

    for param, param_type in func.get("params", {}).items():
        param_type_prediction = parse_type_prediction(param_type)
        if "Unknown" in param_type_prediction:
            continue  # Skip this parameter if the type is unknown
        if " " in param:
            param = param.replace(" ", "_")

        output.append({
            "file": file_name,
            "line_number": fn_lc[0][0],
            "col_offset": fn_lc[0][1],
            "parameter": param,
            "function": name,
            "type": param_type_prediction,          
        })

    for var, var_type in func.get("variables", {}).items():
        var_type_prediction = parse_type_prediction(var_type)
        if "Unknown" in var_type_prediction:
            continue  # Skip this variable if the type is unknown

        if " " in var:
            var = var.replace(" ", "_")  # Replace spaces with underscores

        var_lns = func.get("fn_var_ln", {}).get(var, [])
        
        if not var_lns:
            var.upper()
            var_lns = func.get("fn_var_ln", {}).get(var, [])

        for var_ln in var_lns:
            output.append({
                "file": file_name,
                "line_number": var_ln[0],
                "col_offset": var_ln[1],
                "variable": var,
                "function": name,
                "type": var_type_prediction
            })

if __name__ == "__main__":
    pass