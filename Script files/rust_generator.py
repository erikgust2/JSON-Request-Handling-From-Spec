import json
import os

rust_template = '''
use serde::{{Serialize, Deserialize}};
use serde_json::Result;

#[derive(Serialize, Deserialize)]
pub struct {class_name} {{
{fields}
}}

impl {class_name} {{
    // Serializes the Rust struct into a JSON string
    pub fn serialize(&self) -> Result<String, serde_json::Error> {{
        serde_json::to_string(self).unwrap()
    }}

    // Deserializes the JSON string into a Rust struct
    pub fn deserialize(json_str: &str) -> Result<{class_name}, serde_json::Error> {{
        serde_json::from_str(json_str)
    }}
}}
'''

def load_specification(file_path):
    # Verify the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error decoding JSON from the file '{file_path}': {e}")

def generate_field_code(field):
    rust_type = map_type(field)
    field_name = field['name']
    return f"    pub {field_name}: Option<{rust_type}>,"

def map_type(field):
    rust_type_mapping = {
        "int": "i32",
        "float": "f32",
        "bool": "bool",
        "string": "String",
    }
    basic_type = rust_type_mapping.get(field['type'], "String")
    if field.get("is_array", False):
        return f"Vec<{basic_type}>"
    else:
        return basic_type

def generate_rust_code_from_spec(spec):
    fields = "\n".join(generate_field_code(field) for field in spec['fields'])

    rust_struct_code = rust_template.format(
        class_name=spec['class_name'],
        fields=fields
    )

    rust_file_name = f"../Output/Rust/{spec['class_name'].lower()}.rs"

    with open(rust_file_name, 'w') as file:
        file.write(rust_struct_code)

    print(f"Done! Check the generated Rust code in the file: {rust_file_name}")

if __name__ == "__main__":
    spec = load_specification("../Specs/example_spec.json")
    generate_rust_code_from_spec(spec)
