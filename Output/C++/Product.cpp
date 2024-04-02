
#include <nlohmann/json.hpp>
#include <iostream>
#include <optional>
#include <vector>
#include <map>
using json = nlohmann::json;

enum class tags { electronics, clothing, food };

class Product {
private:
    int id;
    std::string name;
    float price;
    std::optional<std::vector<std::string>> manufacturers;
    bool in_stock;
    std::optional<tags> tag;

public:
    Product() = default;

    std::string serialize() const {
        json j;
        j["id"] = id;
        j["name"] = name;
        j["price"] = price;
        if(manufacturers) j["manufacturers"] = *manufacturers;
        j["in_stock"] = in_stock;
        if(tag) j["tag"] = to_string(*tag);
        return j.dump();
    }

    static Product deserialize(const std::string& json_str) {
        json j = json::parse(json_str);
        Product obj;
        if(!j.contains("id")) throw std::runtime_error("Missing mandatory field: id");
        obj.id = j["id"].get<int>();
        if(!j.contains("name")) throw std::runtime_error("Missing mandatory field: name");
        obj.name = j["name"].get<std::string>();
        if(!j.contains("price")) throw std::runtime_error("Missing mandatory field: price");
        obj.price = j["price"].get<float>();
        obj.manufacturers = j["manufacturers"].get<std::optional<std::vector<std::string>>>();
        if(!j.contains("in_stock")) throw std::runtime_error("Missing mandatory field: in_stock");
        obj.in_stock = j["in_stock"].get<bool>();
        obj.tag = from_string<tags>(j["tag"].get<std::string>());
        return obj;
    }

    int getId() const { return id; }
    void setId(int value) { id = value; }
    std::string getName() const { return name; }
    void setName(std::string value) { name = value; }
    float getPrice() const { return price; }
    void setPrice(float value) { price = value; }
    std::optional<std::vector<std::string>> getManufacturers() const { return manufacturers; }
    void setManufacturers(const std::vector<std::string>& value) { manufacturers = value; }
    bool getIn_stock() const { return in_stock; }
    void setIn_stock(bool value) { in_stock = value; }
    std::optional<tags> getTag() const { return tag; }
    void setTag(const tags& value) { tag = value; }
};
