import json
import os

def load_specification(file_path):
    """Loads the JSON specification from the given file path."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def map_type_to_python(json_type, is_array):
    """Maps JSON types to Python types."""
    type_mapping = {
        "int": "int",
        "float": "float",
        "bool": "bool",
        "string": "str"
    }
    python_type = type_mapping.get(json_type, "str")  # Default to str for unknown types
    if is_array:
        return f"List[{python_type}]"
    else:
        return python_type

def generate_python_class(spec):
    """Generates a Python class with serialization and deserialization methods."""
    fields_str = "\n    ".join([f"{field['name']}: {map_type_to_python(field['type'], field.get('is_array', False))} = field(default_factory=list)"
                                if field.get('is_array', False) 
                                else f"{field['name']}: {map_type_to_python(field['type'], False)} = None"
                                for field in spec['fields']])
    class_str = f"""from dataclasses import dataclass, field, asdict
from typing import List, Optional
import json

@dataclass
class {spec['class_name']}:
    {fields_str}

    @classmethod
    def from_json(cls, json_str: str):
        return cls(**json.loads(json_str))

    def to_json(self) -> str:
        return json.dumps(asdict(self), default=str)
"""
    return class_str

def write_python_file(class_name, python_code):
    """Writes the generated Python code to a file."""
    output_dir = "../Output/Python"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{class_name}.py")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(python_code)
    print(f"Python code has been written to {file_path}")

if __name__ == "__main__":
    spec_path = "../Specs/example_spec.json"  # Update this path as needed
    spec = load_specification(spec_path)
    python_code = generate_python_class(spec)
    write_python_file(spec['class_name'], python_code)
