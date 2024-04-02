
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
        

end Store_Objects;
