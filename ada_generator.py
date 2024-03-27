import json

# Template for the Ada package specification (.ads file)
ada_spec_template = '''
with GNATCOLL.JSON; use GNATCOLL.JSON;

package {package_name} is

    type {type_name} is record
        {fields}
    end record;

    function To_JSON (Item : {type_name}) return JSON_Value;
    function From_JSON (J : JSON_Value) return {type_name};

end {package_name};
'''

# Template for the Ada package body (.adb file)
ada_body_template = '''
with Ada.Text_IO; use Ada.Text_IO;

package body {package_name} is

    function To_JSON (Item : {type_name}) return JSON_Value is
    begin
        return Create_Object
          ({serialization_fields});
    end To_JSON;

    function From_JSON (J : JSON_Value) return {type_name} is
        Result : {type_name};
    begin
        {deserialization_fields}
        return Result;
    end From_JSON;

end {package_name};
'''

def generate_field_code(field):
    ada_type = map_type(field)
    field_name = field['name'].capitalize()
    return f"{field_name} : {ada_type};"

def generate_serialization_code(field):
    field_name = field['name'].capitalize()
    return f'''("{field_name}" => (if Item.{field_name}'Access = null then Null_Value else Item.{field_name}'Access.all'Img))'''

def generate_deserialization_code(field):
    field_name = field['name'].capitalize()
    ada_type = map_type(field, True)
    return f'''Result.{field_name} := (J.Get_Field ("{field_name}").To_{ada_type});'''

def map_type(field, for_deserialization=False):
    basic_type = {
        "int": "Integer",
        "float": "Float",
        "bool": "Boolean",
        "string": "String"
    }.get(field['type'], "String")

    if for_deserialization:
        if field['type'] in ["int", "float"]:
            return basic_type + "_Value"
        elif field['type'] == "bool":
            return "Boolean"
        else:
            return "String"

    return basic_type

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
    fields = "\n        ".join(generate_field_code(field) for field in spec['fields'])
    serialization_fields = ",\n          ".join(generate_serialization_code(field) for field in spec['fields'])
    deserialization_fields = "\n        ".join(generate_deserialization_code(field) for field in spec['fields'])

    ada_spec_code = ada_spec_template.format(
        package_name=spec['package_name'],
        type_name=spec['class_name'],
        fields=fields,
    )
    
    ada_body_code = ada_body_template.format(
        package_name=spec['package_name'],
        type_name=spec['class_name'],
        serialization_fields=serialization_fields,
        deserialization_fields=deserialization_fields
    )

    spec_file_name = f"{spec['package_name']}.ads"
    body_file_name = f"{spec['package_name']}.adb"

    with open(spec_file_name, 'w') as spec_file:
        spec_file.write(ada_spec_code)
        
    with open(body_file_name, 'w') as body_file:
        body_file.write(ada_body_code)

    print(f"Done! Check the generated package specification in the file: {spec_file_name}")
    print(f"Check the generated package body in the file: {body_file_name}")

if __name__ == "__main__":
    spec = load_specification("example_spec.json")
    generate_code_from_spec(spec)
