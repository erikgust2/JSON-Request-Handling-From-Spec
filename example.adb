
with Ada.Text_IO; use Ada.Text_IO;

package body example is

    function To_JSON (Item : request) return JSON_Value is
    begin
        return Create_Object
          (("A" => (if Item.A'Access = null then Null_Value else Item.A'Access.all'Img)),
          ("B" => (if Item.B'Access = null then Null_Value else Item.B'Access.all'Img)),
          ("C" => (if Item.C'Access = null then Null_Value else Item.C'Access.all'Img)),
          ("D" => (if Item.D'Access = null then Null_Value else Item.D'Access.all'Img)));
    end To_JSON;

    function From_JSON (J : JSON_Value) return request is
        Result : request;
    begin
        Result.A := (J.Get_Field ("A").To_Integer_Value);
        Result.B := (J.Get_Field ("B").To_String);
        Result.C := (J.Get_Field ("C").To_Float_Value);
        Result.D := (J.Get_Field ("D").To_Boolean);
        return Result;
    end From_JSON;

end example;
