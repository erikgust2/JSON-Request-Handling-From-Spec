import json

java_template = """
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@JsonInclude(JsonInclude.Include.NON_NULL)
public class {class_name} {{

    {fields}

    public {class_name}() {{ }}

    {getters_setters}

    public static {class_name} deserialize(String json) throws Exception {{
        ObjectMapper objectMapper = new ObjectMapper();
        return objectMapper.readValue(json, {class_name}.class);
    }}

    public String serialize() throws Exception {{
        ObjectMapper objectMapper = new ObjectMapper();
        return objectMapper.writeValueAsString(this);
    }}

    {enums}
}}
"""

def generate_java_code(schema):
    class_name = schema['class_name']
    properties = schema['properties']
    required = schema.get('required', [])

    fields = []
    getters_setters = []
    enums = []

    for prop_name, prop_info in properties.items():
        field_name = prop_name
        field_type = prop_info['type']
        optional = field_name not in required

        if field_type == 'enum':
            enums.append(generate_enum_definition(prop_info))
            java_type = prop_info['enumname']
        else:
            java_type = map_type_to_java(field_type, prop_info)
            if field_type == 'array':
                optional = False  # Arrays are initialized as empty lists, not optional

        fields.append(generate_field_declaration(field_name, java_type, optional, field_type == 'array'))
        getters_setters.append(generate_getters_setters(field_name, java_type, optional, field_type == 'array'))

    return java_template.format(
        class_name=class_name,
        fields="\n    ".join(fields),
        getters_setters="\n    ".join(getters_setters),
        enums="\n    ".join(enums)
    )

def map_type_to_java(json_type, prop_info):
    if json_type == "array":
        item_type = "Object"  # Default item type
        if 'items' in prop_info and 'type' in prop_info['items']:
            item_type = map_type_to_java(prop_info['items']['type'], prop_info['items'])
        return f"List<{item_type}>"
    else:
        mapping = {
            "integer": "Integer",
            "string": "String",
            "number": "Double",
            "boolean": "Boolean",
            "array": "List<Object>"  # Default for arrays without specified item types
        }
        return mapping.get(json_type, "Object")

def generate_enum_definition(prop_info):
    enum_name = prop_info['enumname']
    enum_values = ", ".join([value.upper() for value in prop_info['enum']])
    return f"public enum {enum_name} {{ {enum_values} }};"

def generate_field_declaration(field_name, java_type, optional, is_array):
    if is_array:
        return f"private {java_type} {field_name} = new ArrayList<>();"
    elif optional:
        return f"private Optional<{java_type}> {field_name} = Optional.empty();"
    else:
        return f"private {java_type} {field_name};"

def generate_getters_setters(field_name, java_type, optional, is_array):
    cap_name = field_name.capitalize()
    if is_array or not optional:
        get_set = f"""
    public {java_type} get{cap_name}() {{ return this.{field_name}; }}
    public void set{cap_name}({java_type} {field_name}) {{ this.{field_name} = {field_name}; }}"""
    else:
        get_set = f"""
    public Optional<{java_type}> get{cap_name}() {{ return this.{field_name}; }}
    public void set{cap_name}(Optional<{java_type}> {field_name}) {{ this.{field_name} = {field_name}; }}"""
    return get_set


def load_specification(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_java_code(file_path, java_code):
    with open(file_path, 'w') as file:
        file.write(java_code)

if __name__ == "__main__":
    file_path = "../Specs/example_spec_json_schema.json"
    spec = load_specification(file_path)

    java_code = generate_java_code(spec)

    output_file_path = f"../Output/Java/{spec['class_name']}.java"
    save_java_code(output_file_path, java_code)

    print(f"Generated Java code written to {output_file_path}")
