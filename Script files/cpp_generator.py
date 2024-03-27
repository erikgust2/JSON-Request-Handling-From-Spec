import json

cpp_template = '''
#include <nlohmann/json.hpp>
#include <string>
#include <optional>
using json = nlohmann::json;

class {class_name} {{
private:
    {fields}

public:
    {class_name}() = default; // Default constructor

    // Serializes the C++ Class object into a JSON string
    std::string serialize() const {{
        json j;
        {serialize_optional_fields}
        return j.dump();
    }}

    // Deserializes the JSON string into a C++ Class object
    static {class_name} deserialize(const std::string& json_str) {{
        {class_name} obj;
        try{{
        auto j = json::parse(json_str);
        {deserialize_optional_fields}
        }} catch (const json::exception& e) {{
            std::cerr << "Error parsing JSON: " << e.what() << std::endl;
        }}
        return obj;
    }}

    // Getters and Setters
    {getters_and_setters}
}};
'''

def generate_field_code(field):
    cpp_type = map_type(field)
    field_name = sanitize_name(field['name'])
    return f"std::optional<{cpp_type}> {field_name};"

def generate_serialization_code(field):
    field_name = sanitize_name(field['name'])
    if field.get("is_array", False):
        return f'''if (this->{field_name}) {{\n\t\tj["{field_name}"] = json::array();\n\t\tfor (const auto& item : *this->{field_name}) {{\n\t\t\tj["{field_name}"].emplace_back(item);\n\t\t}}\n\t}}'''
    else:
        return f'''if (this->{field_name}) j["{field_name}"] = *this->{field_name};'''

def generate_deserialization_code(field):
    field_name = sanitize_name(field['name'])
    # Correct the type mapping for array elements
    cpp_type = map_type(field) if not field.get("is_array", False) else f"std::vector<{map_type({'type': field['type'], 'is_array': False})}>"
    if field.get("is_array", False):
        # Fix the handling of map_type for array fields
        return f'''if (j.contains("{field_name}")) {{\n\t\tobj.{field_name} = j["{field_name}"].get<std::optional<{cpp_type}>>();\n\t}}'''
    else:
        # Now correctly closes the if statement
        return f'''if (j.contains("{field_name}")) {{ obj.{field_name} = j.at("{field_name}").get<std::optional<{cpp_type}>>(); }}'''


def generate_getter_setter_code(field):
    cpp_type = map_type(field)
    optional_cpp_type = f"std::optional<{cpp_type}>"
    field_name = sanitize_name(field['name'])
    capitalized_name = field_name.capitalize()

    is_scalar_type = field['type'] in ["int", "float", "bool", "string"]
    setter_argument_type = cpp_type if is_scalar_type else f"const {cpp_type}&"

    getter = f'''const {optional_cpp_type}& get{capitalized_name}() const {{ return {field_name}; }}'''

    setter = f'''void set{capitalized_name}({setter_argument_type} value) {{ {field_name} = value; }}'''
    return getter + "\n\t" + setter

def map_type(field):
    basic_type = {
        "int": "int",
        "float": "float",
        "bool": "bool",
        "string": "std::string"
        # Add more types here as needed
    }.get(field['type'], "void*") # Default to void if the type is not found

    if field.get("is_array", False):
        return f"std::vector<{basic_type}>"
    else:
        return basic_type

def sanitize_name(name):
    cpp_keywords = ["class", "int", "float", "double", "char", "return", "private", "public", "protected", "new", "delete", "void"]
    return f"_{name}" if name in cpp_keywords else name

def load_specification(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} is not a valid JSON file.")
        exit(1)

def generate_code_from_spec(spec):
    fields = "\n\t".join(generate_field_code(field) for field in spec['fields'])
    serialize_optional_fields = "\n\t\t".join(generate_serialization_code(field) for field in spec['fields'])
    deserialize_optional_fields = "\n\t\t".join(generate_deserialization_code(field) for field in spec['fields'])
    getters_setters = "\n\t".join(generate_getter_setter_code(field) for field in spec['fields'])

    cpp_class_code = cpp_template.format(
        class_name=spec['class_name'],
        fields=fields,
        serialize_optional_fields=serialize_optional_fields,
        deserialize_optional_fields=deserialize_optional_fields,
        getters_and_setters=getters_setters
    )

    cpp_file_name = f"../Output/C++/{spec['class_name'].lower()}.cpp"

    with open(cpp_file_name, 'w') as file:
        file.write(cpp_class_code)

    print("Done! Check the generated code in the file: ", cpp_file_name)

if __name__ == "__main__":
    spec = load_specification("../Specs/example_spec.json")
    generate_code_from_spec(spec)