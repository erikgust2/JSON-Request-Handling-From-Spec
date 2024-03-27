
#include <nlohmann/json.hpp>
#include <string>
#include <optional>
using json = nlohmann::json;

class requestY {
private:
    std::optional<int> A
	std::optional<std::string> B
	std::optional<float> C

public:
    requestY() = default; // Default constructor

    // Serializes the C++ Class object into a JSON string
    std::string serialize() const {
        json j;
        if (this->A) j["A"] = *this->A;
		if (this->B) j["B"] = *this->B;
		if (this->C) j["C"] = *this->C;
        return j.dump();
    }

    // Deserializes the JSON string into a C++ Class object
    static requestY deserialize(const std::string& json_str) {
        auto j = json::parse(json_str);
        requestY obj;
        if (j.contains("A") obj.A = j.at("A").get<std::optional<int>>();
		if (j.contains("B") obj.B = j.at("B").get<std::optional<std::string>>();
		if (j.contains("C") obj.C = j.at("C").get<std::optional<float>>();
        return obj;
    }

    // Getters and Setters
    std::optional<int> getA() const { return A; }
    void setA(const std::optional<int>& value) { A = value; }
	std::optional<std::string> getB() const { return B; }
    void setB(const std::optional<std::string>& value) { B = value; }
	std::optional<float> getC() const { return C; }
    void setC(const std::optional<float>& value) { C = value; }
};
