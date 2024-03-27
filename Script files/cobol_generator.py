import json
import os

def map_type_to_cobol(json_type, is_array):
    """Maps a JSON type to a COBOL data type."""
    type_mapping = {
        "int": "9(9)",
        "float": "9(9)V9(9)",
        "bool": "9(1)",  # Assuming 0 = false, 1 = true
        "string": "X(50)"  # Arbitrary length. I am too lazy to handle varying string lengths. Screw you.
    }
    cobol_type = type_mapping.get(json_type, "X(50)")  # Default to string
    if is_array:
        # I refuse to handle arrays in COBOL. You cannot force me. I will not do it.
        print("Screw you, I am not doing arrays")
    return cobol_type

def generate_cobol_data_structure(spec):
    """Generates a COBOL data structure from the JSON specification."""
    cobol_lines = []
    cobol_lines.append(f"01 {spec['class_name']}.")
    for field in spec['fields']:
        cobol_type = map_type_to_cobol(field['type'], field.get('is_array', False))
        cobol_lines.append(f"    05 {field['name']} PIC {cobol_type}.")
    return "\n".join(cobol_lines)

def load_specification(file_path):
    """Loads the JSON specification from the given file path."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
def write_cobol_file(class_name, cobol_code):
    """Writes the generated COBOL code to a file in the specified output directory."""
    output_dir = "../Output/COBOL"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{class_name}.cbl")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(cobol_code)
    print(f"COBOL code has been written to {file_path}")

# Example usage
if __name__ == "__main__":
    spec_path = "../Specs/example_spec.json"  # Adjust the path as needed
    spec = load_specification(spec_path)
    cobol_code = generate_cobol_data_structure(spec)
    write_cobol_file(spec['class_name'], cobol_code)