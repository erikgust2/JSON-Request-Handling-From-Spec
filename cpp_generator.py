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
        auto j = json::parse(json_str);
        {class_name} obj;
        {deserialize_optional_fields}
        return obj;
    }}

    // Getters and Setters
    {getters_and_setters}
}};
'''

def generate_field_code(field):
    cpp_type = map_type(field['type'])
    field_name = sanitize_name(field['name'])
    return f"std::optional<{cpp_type}> {field_name}"

def generate_serialization_code(field):
    field_name = sanitize_name(field['name'])
    return f'''if (this->{field_name}) j["{field_name}"] = *this->{field_name};'''

def generate_deserialization_code(field):
    field_name = sanitize_name(field['name'])
    return f'''if (j.contains("{field_name}") obj.{field_name} = j.at("{field_name}").get<std::optional<{map_type(field['type'])}>>();'''

def generate_getter_setter_code(field):
    cpp_type = f"std::optional<{map_type(field['type'])}>"
    field_name = sanitize_name(field['name'])
    capitalized_name = field_name.capitalize()
    getter = f'''{cpp_type} get{capitalized_name}() const {{ return {field_name}; }}'''
    setter = f'''void set{capitalized_name}(const {cpp_type}& value) {{ {field_name} = value; }}'''
    return getter + "\n    " + setter

def map_type(json_type):
    return {
        "int": "int",
        "float": "float",
        "string": "std::string"

        # Add more types here as needed

    }.get(json_type, "void*") # Default to void if the type is not found

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

    cpp_file_name = f"{spec['class_name'].lower()}.cpp"

    with open(cpp_file_name, 'w') as file:
        file.write(cpp_class_code)

    print("Done! Check the generated code in the file: ", cpp_file_name)

if __name__ == "__main__":
    spec = load_specification("example_spec.json")
    generate_code_from_spec(spec)