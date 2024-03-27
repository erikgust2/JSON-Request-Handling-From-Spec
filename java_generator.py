import json

java_template = '''
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.JsonProcessingException;
import java.io.IOException;
import java.util.List;
import java.util.Optional;

public class {class_name} {{
    private static final ObjectMapper mapper = new ObjectMapper();
    {fields}

    public {class_name}() {{}} // Default constructor

    // Serializes the Java class object into a JSON string
    public String serialize() {{
        try {{
            return mapper.writeValueAsString(this);
        }} catch (JsonProcessingException e) {{
            e.printStackTrace();
            return null;
        }}
    }}

    // Deserializes the JSON string into a Java class object
    public static {class_name} deserialize(String jsonStr) {{
        try {{
            return mapper.readValue(jsonStr, {class_name}.class);
        }} catch (IOException e) {{
            e.printStackTrace();
            return null;
        }}
    }}

    // Getters and Setters
    {getters_and_setters}
}}
'''

def generate_field_code(field):
    field_name = sanitize_name(field['name'])
    if field.get("is_array", False):
        java_type = f"List<{map_type(field)}>"
        return f"private {java_type} {field_name} = new ArrayList<>();"
    else:
        java_type = map_type(field)
        return f"private Optional<{java_type}> {field_name} = Optional.empty();"

def generate_getter_setter_code(field):
    field_name = sanitize_name(field['name'])
    capitalized_name = field_name.capitalize()

    if field.get("is_array", False):
        java_type = f"List<{map_type(field)}>"
        getter = f'''public {java_type} get{capitalized_name}() {{ return {field_name}; }}'''
        setter = f'''public void set{capitalized_name}({java_type} {field_name}) {{ this.{field_name} = {field_name}; }}'''
    else:
        java_type = map_type(field)
        getter = f'''public Optional<{java_type}> get{capitalized_name}() {{ return {field_name}; }}'''
        setter = f'''public void set{capitalized_name}(Optional<{java_type}> {field_name}) {{ this.{field_name} = {field_name}; }}'''

    return getter + "\n    " + setter

def map_type(field):
    basic_type = {
        "int": "Integer",
        "float": "Float",
        "bool": "Boolean",
        "string": "String"
    }.get(field['type'], "Object")

    if field.get("is_array", False):
        return basic_type
    else:
        return basic_type

def sanitize_name(name):
    java_keywords = ["class", "int", "float", "double", "char", "return", "private", "public", "protected", "new", "delete", "void"]
    return f"_{name}" if name in java_keywords else name

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
    fields = "\n    ".join(generate_field_code(field) for field in spec['fields'])
    getters_setters = "\n    ".join(generate_getter_setter_code(field) for field in spec['fields'])

    java_class_code = java_template.format(
        class_name=spec['class_name'],
        fields=fields,
        getters_and_setters=getters_setters
    )

    java_file_name = f"{spec['class_name']}.java"

    with open(java_file_name, 'w') as file:
        file.write(java_class_code)

    print("Done! Check the generated code in the file: ", java_file_name)


if __name__ == "__main__":
    spec = load_specification("example_spec.json")
    generate_code_from_spec(spec)