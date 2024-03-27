
with GNATCOLL.JSON; use GNATCOLL.JSON;

package example is

    type request is record
        A : Integer;
        B : String;
        C : Float;
        D : Boolean;
    end record;

    function To_JSON (Item : request) return JSON_Value;
    function From_JSON (J : JSON_Value) return request;

end example;
