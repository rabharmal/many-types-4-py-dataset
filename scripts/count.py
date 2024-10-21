import json

# Function to count the types from the data read from JSON
def count_types_from_json(file_path):
    # Read JSON data from the file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Counters for function return types, parameter types, and variable types
    function_return_count = 0
    parameter_count = 0
    variable_count = 0
    variable_no_line_number_count = 0  # Counter for variables without line numbers

    # Counters for known and unknown types
    known_function_return_count = 0
    unknown_function_return_count = 0
    known_parameter_count = 0
    unknown_parameter_count = 0
    known_variable_count = 0
    unknown_variable_count = 0

    # Total count of objects
    total_count = len(data)

    # Iterate over each object in the list
    for obj in data:
        obj_type = obj.get("type", ["Unknown"])  # Ensure type is always a list
        if isinstance(obj_type, list):
            is_known = "Unknown" not in obj_type and obj_type  # Check if it's a known type

        # Check for function return type (key "function" with no "parameter" or "variable")
        if "function" in obj and "parameter" not in obj and "variable" not in obj:
            function_return_count += 1
            if is_known:
                known_function_return_count += 1
            else:
                unknown_function_return_count += 1

        # Check for parameter type (key "parameter" present)
        elif "parameter" in obj:
            parameter_count += 1
            if is_known:
                known_parameter_count += 1
            else:
                unknown_parameter_count += 1

        # Check for variable type (key "variable" present)
        elif "variable" in obj:
            variable_count += 1
            if is_known:
                known_variable_count += 1
            else:
                unknown_variable_count += 1

            # Check if the variable has no line number
            if "line_number" not in obj:
                variable_no_line_number_count += 1

    # Calculate percentages
    function_return_known_percentage = (known_function_return_count / function_return_count * 100) if function_return_count > 0 else 0
    parameter_known_percentage = (known_parameter_count / parameter_count * 100) if parameter_count > 0 else 0
    variable_known_percentage = (known_variable_count / variable_count * 100) if variable_count > 0 else 0

    # Output the counts and percentages
    print("Function return type count:", function_return_count)
    print("Known function return type count:", known_function_return_count)
    print("Unknown function return type count:", unknown_function_return_count)
    print(f"Percentage of known function return types: {function_return_known_percentage:.2f}%\n")

    print("Parameter type count:", parameter_count)
    print("Known parameter type count:", known_parameter_count)
    print("Unknown parameter type count:", unknown_parameter_count)
    print(f"Percentage of known parameter types: {parameter_known_percentage:.2f}%\n")

    print("Variable type count:", variable_count)
    print("Known variable type count:", known_variable_count)
    print("Unknown variable type count:", unknown_variable_count)
    print(f"Percentage of known variable types: {variable_known_percentage:.2f}%\n")

    print("Variables without line numbers:", variable_no_line_number_count)
    print("Total count of objects:", total_count)

# Path to the JSON file
file_path = '../split_dataset/valid_translated.json'

# Call the function with the file path
count_types_from_json(file_path)