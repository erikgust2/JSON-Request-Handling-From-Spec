
package Store_Objects is

   type Product is tagged private;

   type tags is ( electronics,
      clothing,
      food );

   function Get_id(Self : Product) return Integer;
   procedure Set_id(Self : in out Product; Value : Integer);
   function Get_name(Self : Product) return Unbounded_String;
   procedure Set_name(Self : in out Product; Value : Unbounded_String);
   function Get_price(Self : Product) return Float;
   procedure Set_price(Self : in out Product; Value : Float);
   function Get_manufacturers(Self : Product) return GNATCOLL.JSON.JSON_Array;
   function Get_in_stock(Self : Product) return Boolean;
   procedure Set_in_stock(Self : in out Product; Value : Boolean);
   function Get_tag(Self : Product) return tags;
   procedure Set_tag(Self : in out Product; Value : tags);

private
   id : Integer;
   name : Unbounded_String;
   price : Float;
   manufacturers : GNATCOLL.JSON.JSON_Array;
   in_stock : Boolean;
   tag : tags;

end Store_Objects;
