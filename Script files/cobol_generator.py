import json
import os

def map_type_to_cobol(json_type, is_array):
    """Maps a JSON type to a COBOL data type. Because why not bring a 60s language to the JSON era?"""
    type_mapping = {
        "int": "9(9)",  # Because who needs more than 9 digits?
        "float": "9(9)V9(9)",  # Floating points in COBOL, because precision is just a suggestion.
        "bool": "9(1)",  # Booleans in COBOL: a tale of 0s and 1s pretending to be false and true.
        "string": "X(50)"  # Fixed length because COBOL doesn't believe in variability. Or joy.
    }
    cobol_type = type_mapping.get(json_type, "X(50)")  # Defaulting to string because, honestly, who cares anymore?

    if is_array:
        # Look, if you wanted arrays, you picked the wrong half-century.
        print("You thought arrays were bad in modern languages? Hah, cute. No arrays for you.")
    return cobol_type

def generate_cobol_data_structure(spec):
    """Generates a COBOL data structure from the JSON specification. As if COBOL cared about your JSON."""
    cobol_lines = [f"01 {spec['class_name'].upper()}.  * Because everything is better in uppercase."]
    for field in spec['fields']:
        cobol_type = map_type_to_cobol(field['type'], field.get('is_array', False))
        cobol_lines.append(f"    05 {field['name'].upper()} PIC {cobol_type}.  * Dynamic typing is overrated anyway.")
    cobol_lines.append("\n* Here's where you'd serialize, if COBOL had any idea what JSON was.")
    cobol_lines.append("* Deserialization? In COBOL? Good luck, brave soul.")
    return "\n".join(cobol_lines)

def load_specification(file_path):
    """Loads the JSON specification from the given path, as if preparing for a ritual."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
def write_cobol_file(class_name, cobol_code):
    """Writes the generated COBOL code to a file, like etching runes into stone."""
    output_dir = "../Output/COBOL"
    os.makedirs(output_dir, exist_ok=True)  # Behold, the directory emerges from the void.
    file_path = os.path.join(output_dir, f"{class_name}.cbl")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(cobol_code)
    print(f"COBOL code has been etched into {file_path}. May the ancients have mercy on your soul.")

# Let the ritual begin
if __name__ == "__main__":
    spec_path = "../Specs/example_spec.json"  # Adjust path as needed, or let it adjust you.
    spec = load_specification(spec_path)
    cobol_code = generate_cobol_data_structure(spec)
    write_cobol_file(spec['class_name'], cobol_code)