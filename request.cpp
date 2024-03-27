
#include <nlohmann/json.hpp>
#include <string>
#include <optional>
using json = nlohmann::json;

class request {
private:
    std::optional<int> A;
	std::optional<std::string> B;
	std::optional<float> C;
	std::optional<std::vector<bool>> D;

public:
    request() = default; // Default constructor

    // Serializes the C++ Class object into a JSON string
    std::string serialize() const {
        json j;
        if (this->A) j["A"] = *this->A;
		if (this->B) j["B"] = *this->B;
		if (this->C) j["C"] = *this->C;
		if (this->D) {
		j["D"] = json::array();
		for (const auto& item : *this->D) {
			j["D"].emplace_back(item);
		}
	}
        return j.dump();
    }

    // Deserializes the JSON string into a C++ Class object
    static request deserialize(const std::string& json_str) {
        request obj;
        try{
        auto j = json::parse(json_str);
        if (j.contains("A")) { obj.A = j.at("A").get<std::optional<int>>(); }
		if (j.contains("B")) { obj.B = j.at("B").get<std::optional<std::string>>(); }
		if (j.contains("C")) { obj.C = j.at("C").get<std::optional<float>>(); }
		if (j.contains("D")) {
		obj.D = j["D"].get<std::optional<std::vector<bool>>>();
	}
        } catch (const json::exception& e) {
            std::cerr << "Error parsing JSON: " << e.what() << std::endl;
        }
        return obj;
    }

    // Getters and Setters
    const std::optional<int>& getA() const { return A; }
	void setA(int value) { A = value; }
	const std::optional<std::string>& getB() const { return B; }
	void setB(std::string value) { B = value; }
	const std::optional<float>& getC() const { return C; }
	void setC(float value) { C = value; }
	const std::optional<std::vector<bool>>& getD() const { return D; }
	void setD(std::vector<bool> value) { D = value; }
};
