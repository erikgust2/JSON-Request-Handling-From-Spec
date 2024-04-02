
with Ada.Strings.Unbounded; use Ada.Strings.Unbounded;
with GNATCOLL.JSON; use GNATCOLL.JSON;

package body Store_Objects is

   
   function Get_id(Self : Product) return Integer is
   begin
      return Self.id;
   end Get_id;

   procedure Set_id(Self : in out Product; Value : Integer) is
   begin
      Self.id := Value;
   end Set_id;
        

   function Get_name(Self : Product) return Unbounded_String is
   begin
      return Self.name;
   end Get_name;

   procedure Set_name(Self : in out Product; Value : Unbounded_String) is
   begin
      Self.name := Value;
   end Set_name;
        

   function Get_price(Self : Product) return Float is
   begin
      return Self.price;
   end Get_price;

   procedure Set_price(Self : in out Product; Value : Float) is
   begin
      Self.price := Value;
   end Set_price;
        

   function Get_manufacturers(Self : Product) return GNATCOLL.JSON.JSON_Array is
   begin
      return Self.manufacturers;
   end Get_manufacturers;

   procedure Set_manufacturers(Self : in out Product; Value : GNATCOLL.JSON.JSON_Array) is
   begin
      Self.manufacturers := Value;
   end Set_manufacturers;
        

   function Get_in_stock(Self : Product) return Boolean is
   begin
      return Self.in_stock;
   end Get_in_stock;

   procedure Set_in_stock(Self : in out Product; Value : Boolean) is
   begin
      Self.in_stock := Value;
   end Set_in_stock;
        

   function Get_tag(Self : Product) return tags is
   begin
      return Self.tag;
   end Get_tag;

   procedure Set_tag(Self : in out Product; Value : tags) is
   begin
      Self.tag := Value;
   end Set_tag;
        
   function To_JSON (Self : Product) return GNATCOLL.JSON.JSON_Value'Class is
      J : GNATCOLL.JSON.JSON_Object := GNATCOLL.JSON.Create_Object;
   begin
      J.Set_Field ("id", GNATCOLL.JSON.To_JSON (Self.id));
      J.Set_Field ("name", GNATCOLL.JSON.Create_String (To_Unbounded_String (Self.name)));
      J.Set_Field ("price", GNATCOLL.JSON.To_JSON (Self.price));
      -- Array serialization needs custom handling based on array content type
      J.Set_Field ("manufacturers", GNATCOLL.JSON.To_JSON (Your_Array_To_JSON_Function (Self.manufacturers)));
      J.Set_Field ("in_stock", GNATCOLL.JSON.To_JSON (Self.in_stock));
      J.Set_Field ("tag", GNATCOLL.JSON.To_JSON (GNATCOLL.JSON.Create_String (To_String (Self.tag))));
      return GNATCOLL.JSON.JSON_Value'Class (J);
   end To_JSON;
   procedure From_JSON (Self : out Product; J : GNATCOLL.JSON.JSON_Value'Class) is
      Obj : GNATCOLL.JSON.JSON_Object := GNATCOLL.JSON.To_Object (J);
   begin
      Self.id := GNATCOLL.JSON.Get_Integer (Obj.Get_Field ("id"));
      Self.name := To_String (GNATCOLL.JSON.Get_Unbounded_String (Obj.Get_Field ("name")));
      Self.price := GNATCOLL.JSON.Get_Number (Obj.Get_Field ("price"));
      -- Array deserialization needs custom handling based on array content type
      Your_JSON_To_Array_Function (Obj.Get_Field ("manufacturers"), Self.manufacturers);
      Self.in_stock := GNATCOLL.JSON.Get_Boolean (Obj.Get_Field ("in_stock"));
      Self.tag := To_tags (GNATCOLL.JSON.Get_String (Obj.Get_Field ("tag")));
   end From_JSON;

end Store_Objects;
