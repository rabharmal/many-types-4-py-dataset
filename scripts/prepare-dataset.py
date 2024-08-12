import json
import os
from glob import glob

# Define the directory containing the JSON files and the base directory for source files
json_directory = '../downloaded-dataset/ManyTypes4PyDataset-v0.7/processed_projects_clean'
base_directory = '../'

# Output dictionaries to collect data, keyed by split type and then by project
output_data = {
    'train': {},
    'test': {},
    'valid': {}
}

def read_file_content(file_path):
    """Reads the content of a file and returns it as a string."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return ""
    except Exception as e:
        print(f"An error occurred while reading {file_path}: {e}")
        return ""

def update_json(json_path, base_dir):
    """Updates the JSON by adding 'source_code' to each object in 'src_files' and splitting data."""
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"File not found: {json_path}")
        return
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {json_path}")
        return
    except Exception as e:
        print(f"An error occurred while reading {json_path}: {e}")
        return

    for project_name, project_data in data.items():
        if 'src_files' in project_data:
            for file_name, attributes in project_data['src_files'].items():
                # Construct the full path to the source file
                full_path = os.path.join(base_dir, file_name)
                
                # Read the file content
                file_content = read_file_content(full_path)
                
                # Add or update the "source_code" key-value pair
                attributes["source_code"] = file_content
                
                # If file is empty then skip to add it in the output_data
                if file_content == "":
                    print(f"Empty file: {full_path}")
                    continue
                
                # Determine the split type (train, test, valid) and populate output_data
                split_type = attributes.get("set")
                if split_type in ['train', 'test', 'valid']:
                    if project_name not in output_data[split_type]:
                        output_data[split_type][project_name] = {"src_files": {}}
                    output_data[split_type][project_name]['src_files'][file_name] = attributes

    # Write the updated JSON back to the file
    try:
        with open(json_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"An error occurred while writing {json_path}: {e}")
        return

    print(f"JSON file updated successfully: {json_path}")

def process_json_files_in_directory(directory, base_dir):
    """Processes all JSON files in the specified directory."""
    # List all files in the directory
    for file_name in os.listdir(directory):
        if file_name.endswith('.json'):
            json_path = os.path.join(directory, file_name)
            update_json(json_path, base_dir)

    # Write the split data to respective JSON files
    for split_type, projects in output_data.items():
        output_file_path = (f'../split_data/{split_type}.json')
        try:
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                json.dump(projects, output_file, indent=4)
            print(f"{split_type}.json file created successfully.")
        except Exception as e:
            print(f"An error occurred while writing {split_type}.json: {e}")

# Run the script
process_json_files_in_directory(json_directory, base_directory)