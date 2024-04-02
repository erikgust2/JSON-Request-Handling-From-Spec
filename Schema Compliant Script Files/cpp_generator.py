import json

cpp_template = '''
#include <nlohmann/json.hpp>
#include <iostream>
#include <optional>
#include <vector>
#include <map>
using json = nlohmann::json;

{enum_definitions}

class {class_name} {{
private:
    {fields}

public:
    {class_name}() = default;

    std::string serialize() const {{
        json j;
        {serialize_fields}
        return j.dump();
    }}

    static {class_name} deserialize(const std::string& json_str) {{
        json j = json::parse(json_str);
        {class_name} obj;
        {deserialize_fields}
        return obj;
    }}

    {getters_and_setters}
}};
'''

def generate_enum_definitions(enums):
    enum_definitions = []
    for enum_name, values in enums.items():
        enum_cases = ', '.join(values)
        enum_definition = f"enum class {enum_name} {{ {enum_cases} }};"
        enum_definitions.append(enum_definition)
    return '\n'.join(enum_definitions) if enums else ""

def map_type(field):
    type_mappings = {
        "integer": "int",
        "number": "float",
        "string": "std::string",
        "boolean": "bool",
        "array": "std::vector", 
    }
    cpp_type = type_mappings.get(field.get("type", ""), "void*")
    if field.get("type") == "array":
        item_type = map_type(field.get("items", {}))  # Recursively map the item type
        cpp_type = f"{type_mappings['array']}<{item_type}>"
    return cpp_type


def generate_field_declaration(field_name, field_def, required_fields):
    is_required = field_name in required_fields
    cpp_type = map_type(field_def) if field_def['type'] != 'enum' else field_def['enumname']
    field_type = cpp_type if is_required else f"std::optional<{cpp_type}>"
    return f"{field_type} {field_name};"

def generate_serialize_code(field_name, field_def, required_fields):
    is_required = field_name in required_fields
    if field_def['type'] == 'enum':
        return f'if({field_name}) j["{field_name}"] = to_string(*{field_name});' if not is_required else f'j["{field_name}"] = to_string({field_name});'
    else:
        return f'if({field_name}) j["{field_name}"] = *{field_name};' if not is_required else f'j["{field_name}"] = {field_name};'

def generate_deserialize_code(field_name, field_def, required_fields):
    is_required = field_name in required_fields
    cpp_type = map_type(field_def) if field_def['type'] != 'enum' else field_def['enumname']
    field_type = cpp_type if is_required else f"std::optional<{cpp_type}>"
    deserialization_code = ""
    if is_required:
        deserialization_code += f'if(!j.contains("{field_name}")) throw std::runtime_error("Missing mandatory field: {field_name}");\n        '
    if field_def['type'] == 'enum':
        deserialization_code += f'obj.{field_name} = from_string<{cpp_type}>(j["{field_name}"].get<std::string>());'
    else:
        deserialization_code += f'obj.{field_name} = j["{field_name}"].get<{field_type}>();'
    return deserialization_code

def generate_getter_setter(field_name, field_def, required_fields):
    is_required = field_name in required_fields
    cpp_type = map_type(field_def) if field_def['type'] != 'enum' else field_def['enumname']
    field_type = cpp_type if is_required else f"std::optional<{cpp_type}>"
    getter = f"{field_type} get{field_name.capitalize()}() const {{ return {field_name}; }}"
    setter_arg = cpp_type if is_required else f"const {cpp_type}&"
    setter = f"void set{field_name.capitalize()}({setter_arg} value) {{ {field_name} = value; }}"
    return getter, setter

def generate_code_from_spec(spec):
    # Extracting enum definitions correctly
    enums = {}
    for field_name, field_def in spec['properties'].items():
        if isinstance(field_def, dict) and field_def.get('type') == 'enum':
            enums[field_def['enumname']] = field_def['enum']

    # Correctly extracting required fields
    required_fields = spec.get('required', [])  # This should always result in a list

    fields = []
    serialize_fields = []
    deserialize_fields = []
    getters_and_setters = []

    for field_name, field_def in spec['properties'].items():
        if isinstance(field_def, dict):  # Making sure field_def is a dictionary
            fields.append(generate_field_declaration(field_name, field_def, required_fields))
            serialize_fields.append(generate_serialize_code(field_name, field_def, required_fields))
            deserialize_fields.append(generate_deserialize_code(field_name, field_def, required_fields))
            getter, setter = generate_getter_setter(field_name, field_def, required_fields)
            getters_and_setters.extend([getter, setter])

    enum_definitions = generate_enum_definitions(enums)
    class_definition = cpp_template.format(
        class_name=spec['class_name'],
        fields='\n    '.join(fields),
        serialize_fields='\n        '.join(serialize_fields),
        deserialize_fields='\n        '.join(deserialize_fields),
        getters_and_setters='\n    '.join(getters_and_setters),
        enum_definitions=enum_definitions
    )
    return class_definition

def load_specification(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    file_path = "../Specs/example_spec_json_schema.json"  # Specify your JSON schema file path here
    spec = load_specification(file_path)
    cpp_code = generate_code_from_spec(spec)
    
    output_file_path = f"../Output/C++/{spec['class_name']}.cpp"  # Output file named after the class
    with open(output_file_path, 'w') as file:
        file.write(cpp_code)
    print(f"Generated C++ code written to {output_file_path}")
