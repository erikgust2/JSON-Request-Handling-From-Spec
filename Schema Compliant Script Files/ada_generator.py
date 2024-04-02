import json

# Templates for Ada package specification (.ads) and body (.adb)
ads_template = '''
package {package_name} is

   type {class_name} is tagged private;

   {enum_definitions}

   -- Public subprograms including getters, setters, and serialization/deserialization functions
   {public_subprograms}

   function To_JSON (Self : {class_name}) return GNATCOLL.JSON.JSON_Value'Class;
   procedure From_JSON (Self : out {class_name}; J : GNATCOLL.JSON.JSON_Value'Class);

private
   {private_types}

end {package_name};
'''

adb_template = '''
with Ada.Strings.Unbounded; use Ada.Strings.Unbounded;
with GNATCOLL.JSON; use GNATCOLL.JSON;

package body {package_name} is

   {body_subprograms}

end {package_name};
'''

def generate_enum_definitions(enums):
    enum_definitions = []
    for enum_name, values in enums.items():
        enum_body = ',\n      '.join(values)
        enum_definition = f"type {enum_name} is ( {enum_body} );"
        enum_definitions.append(enum_definition)
    return '\n   '.join(enum_definitions) if enums else ""

def map_type(field):
    type_mappings = {
        "integer": "Integer",
        "number": "Float",
        "string": "Unbounded_String",
        "boolean": "Boolean",
        "array": "GNATCOLL.JSON.JSON_Array"
    }
    ada_type = type_mappings.get(field.get("type", ""), "access GNATCOLL.JSON.JSON_Value'Class")
    return ada_type

def generate_field_declaration(field_name, field_def, required_fields):
    ada_type = map_type(field_def) if field_def['type'] != 'enum' else field_def['enumname']
    return f"{field_name} : {ada_type};"

def generate_public_subprograms(class_name, fields, enums):
    getters_and_setters = []
    for field in fields:
        field_name, field_def = field
        ada_type = map_type(field_def) if field_def['type'] != 'enum' else field_def['enumname']
        getters_and_setters.append(f"function Get_{field_name}(Self : {class_name}) return {ada_type};")
        if field_def['type'] != 'array':  # Arrays might not have a simple setter
            getters_and_setters.append(f"procedure Set_{field_name}(Self : in out {class_name}; Value : {ada_type});")
    return '\n   '.join(getters_and_setters)

def generate_body_subprograms(class_name, fields, enums):
    subprograms = []
    for field in fields:
        field_name, field_def = field
        ada_type = map_type(field_def) if field_def['type'] != 'enum' else field_def['enumname']
        subprograms.append(f'''
   function Get_{field_name}(Self : {class_name}) return {ada_type} is
   begin
      return Self.{field_name};
   end Get_{field_name};

   procedure Set_{field_name}(Self : in out {class_name}; Value : {ada_type}) is
   begin
      Self.{field_name} := Value;
   end Set_{field_name};
        ''')
    return '\n'.join(subprograms)

def generate_serialization_subprograms(class_name, fields):
    serialization_procedures = f'''
   function To_JSON (Self : {class_name}) return GNATCOLL.JSON.JSON_Value'Class is
      J : GNATCOLL.JSON.JSON_Object := GNATCOLL.JSON.Create_Object;
   begin'''
    for field_name, field_def in fields:
        field_type = field_def.get('type')
        if field_type == 'enum':
            serialization_procedures += f'''
      J.Set_Field ("{field_name}", GNATCOLL.JSON.To_JSON (GNATCOLL.JSON.Create_String (To_String (Self.{field_name}))));'''
        elif field_type in ['integer', 'number']:
            serialization_procedures += f'''
      J.Set_Field ("{field_name}", GNATCOLL.JSON.To_JSON (Self.{field_name}));'''
        elif field_type == 'string':
            serialization_procedures += f'''
      J.Set_Field ("{field_name}", GNATCOLL.JSON.Create_String (To_Unbounded_String (Self.{field_name})));'''
        elif field_type == 'boolean':
            serialization_procedures += f'''
      J.Set_Field ("{field_name}", GNATCOLL.JSON.To_JSON (Self.{field_name}));'''
        elif field_type == 'array':
            serialization_procedures += f'''
      -- Array serialization needs custom handling based on array content type
      J.Set_Field ("{field_name}", GNATCOLL.JSON.To_JSON (Your_Array_To_JSON_Function (Self.{field_name})));'''
    serialization_procedures += '''
      return GNATCOLL.JSON.JSON_Value'Class (J);
   end To_JSON;'''

    return serialization_procedures

def generate_deserialization_subprograms(class_name, fields):
    deserialization_procedures = f'''
   procedure From_JSON (Self : out {class_name}; J : GNATCOLL.JSON.JSON_Value'Class) is
      Obj : GNATCOLL.JSON.JSON_Object := GNATCOLL.JSON.To_Object (J);
   begin'''
    for field_name, field_def in fields:
        field_type = field_def.get('type')
        if field_type == 'enum':
            deserialization_procedures += f'''
      Self.{field_name} := To_{field_def['enumname']} (GNATCOLL.JSON.Get_String (Obj.Get_Field ("{field_name}")));'''
        elif field_type in ['integer', 'number']:
            deserialization_procedures += f'''
      Self.{field_name} := GNATCOLL.JSON.Get_{field_type.capitalize()} (Obj.Get_Field ("{field_name}"));'''
        elif field_type == 'string':
            deserialization_procedures += f'''
      Self.{field_name} := To_String (GNATCOLL.JSON.Get_Unbounded_String (Obj.Get_Field ("{field_name}")));'''
        elif field_type == 'boolean':
            deserialization_procedures += f'''
      Self.{field_name} := GNATCOLL.JSON.Get_Boolean (Obj.Get_Field ("{field_name}"));'''
        elif field_type == 'array':
            deserialization_procedures += f'''
      -- Array deserialization needs custom handling based on array content type
      Your_JSON_To_Array_Function (Obj.Get_Field ("{field_name}"), Self.{field_name});'''
    deserialization_procedures += '''
   end From_JSON;'''

    return deserialization_procedures

def generate_code_from_spec(spec):
    # Extract enums and required fields
    enums = {f['enumname']: f['enum'] for _, f in spec['properties'].items() if f.get('type') == 'enum'}
    required_fields = spec.get('required', [])
    fields = [(name, defn) for name, defn in spec['properties'].items()]

    # Generate Ada package specification and body components
    enum_definitions = generate_enum_definitions(enums)
    private_types = '\n   '.join([generate_field_declaration(f[0], f[1], required_fields) for f in fields])
    public_subprograms = generate_public_subprograms(spec['class_name'], fields, enums)
    body_subprograms = generate_body_subprograms(spec['class_name'], fields, enums)

    serialization_code = generate_serialization_subprograms(spec['class_name'], [(name, defn) for name, defn in spec['properties'].items()])
    deserialization_code = generate_deserialization_subprograms(spec['class_name'], [(name, defn) for name, defn in spec['properties'].items()])

    body_subprograms += serialization_code + deserialization_code

    # Fill in templates
    ads_code = ads_template.format(
        package_name=spec['package_name'],
        class_name=spec['class_name'],
        enum_definitions=enum_definitions,
        public_subprograms=public_subprograms,
        private_types=private_types
    )

    adb_code = adb_template.format(
        package_name=spec['package_name'],
        body_subprograms=body_subprograms
    )

    return ads_code, adb_code

def load_specification(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    file_path = "../Specs/example_spec_json_schema.json"  # Specify your JSON schema file path here
    spec = load_specification(file_path)
    ads_code, adb_code = generate_code_from_spec(spec)
    
    # Output Ada package specification
    with open(f"{spec['package_name']}.ads", 'w') as ads_file:
        ads_file.write(ads_code)
    
    # Output Ada package body
    with open(f"{spec['package_name']}.adb", 'w') as adb_file:
        adb_file.write(adb_code)
    
    print(f"Generated Ada code written to {spec['package_name']}.ads and {spec['package_name']}.adb")
