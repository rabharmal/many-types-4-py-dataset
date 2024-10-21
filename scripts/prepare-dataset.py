import json
import os
from translator_x import translate_content

# Define the directory containing the JSON files and the base directory for source files
json_directory = '/home/rashida/tools/rashida-thesis/many-types-4-py-dataset/downloaded-dataset/ManyTypes4PyDataset-v0.7/processed_projects_clean'
base_directory = '/home/rashida/tools/rashida-thesis/many-types-4-py-dataset'

# Output dictionaries to collect data, keyed by split type and then by project
output_data = {
    'train': {},
    'test': {},
    'valid': {}
}

# Counter for non-deleted JSON files
non_deleted_json_count = 0

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
    global non_deleted_json_count  # Allow modification of the counter

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

    all_files_missing = True  # Track if all source files are missing for deletion

    for project_name, project_data in data.items():
        if 'src_files' in project_data:
            for file_name, attributes in project_data['src_files'].items():
                # Construct the full path to the source file
                full_path = os.path.join(base_dir, file_name)
                
                # Read the file content
                file_content = read_file_content(full_path)
                
                # If the source file is found, mark that not all files are missing
                if file_content != "":
                    all_files_missing = False

                # Add or update the "source_code" key-value pair
                attributes["source_code"] = file_content
                
                split_type = attributes.get("set")

                # Populate output_data for each split type
                if split_type in ['train', 'test', 'valid']:
                    if project_name not in output_data[split_type]:
                        output_data[split_type][project_name] = {"src_files": {}}
                    output_data[split_type][project_name]['src_files'][file_name] = attributes
                else:
                    print(f"Unknown split type for project '{project_name}': {split_type}")

    if all_files_missing:
        # Delete the JSON file only if all source files are missing
        try:
            os.remove(json_path)
            print(f"Deleted JSON file because all source files were missing: {json_path}")
        except Exception as e:
            print(f"An error occurred while deleting {json_path}: {e}")
    else:
        # Write the updated JSON back to the file if at least one source file was found
        try:
            with open(json_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            print(f"JSON file updated successfully: {json_path}")
            # Increment the counter for non-deleted JSON files
            non_deleted_json_count += 1
        except Exception as e:
            print(f"An error occurred while writing {json_path}: {e}")
            return

def process_json_files_in_directory(directory, base_dir):
    """Processes all JSON files in the specified directory."""
    # List all files in the directory
    for file_name in os.listdir(directory):
        if file_name.endswith('.json'):
            json_path = os.path.join(directory, file_name)
            update_json(json_path, base_dir)

    # Write the split data to respective JSON files
    for split_type, projects in output_data.items():
        output_file_path = os.path.join(base_dir, 'split_dataset', f'{split_type}.json')
        try:
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                json.dump(projects, output_file, indent=4)
            print(f"{split_type}.json file created successfully.")
        except Exception as e:
            print(f"An error occurred while writing {split_type}.json: {e}")

    # Output the count of non-deleted JSON files
    print(f"Number of JSON files not deleted: {non_deleted_json_count}")

def translate_and_save_json_files(split_data_directory):
    splits = ['train', 'test', 'valid']
    for split in splits:
        input_file_path = f'{split_data_directory}/{split}.json'
        output_file_path = f'{split_data_directory}/{split}_translated.json'

        try:
            with open(input_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            translated_data = translate_content(data)

            with open(output_file_path, 'w', encoding='utf-8') as file:
                json.dump(translated_data, file, indent=4)
            print(f"Translated {split}.json file saved to {output_file_path}")
        except FileNotFoundError:
            print(f"File not found: {input_file_path}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {input_file_path}")
        except Exception as e:
            print(f"An error occurred during the translation of {input_file_path}: {e}")

# Run the script
process_json_files_in_directory(json_directory, base_directory)
translate_and_save_json_files('/home/rashida/tools/rashida-thesis/many-types-4-py-dataset/split_dataset')  # Adjust the path as needed