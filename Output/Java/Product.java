
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@JsonInclude(JsonInclude.Include.NON_NULL)
public class Product {

    private Integer id;
    private String name;
    private Double price;
    private List<String> manufacturers = new ArrayList<>();
    private Boolean in_stock;
    private Optional<tags> tag = Optional.empty();

    public Product() { }

    
    public Integer getId() { return this.id; }
    public void setId(Integer id) { this.id = id; }
    
    public String getName() { return this.name; }
    public void setName(String name) { this.name = name; }
    
    public Double getPrice() { return this.price; }
    public void setPrice(Double price) { this.price = price; }
    
    public List<String> getManufacturers() { return this.manufacturers; }
    public void setManufacturers(List<String> manufacturers) { this.manufacturers = manufacturers; }
    
    public Boolean getIn_stock() { return this.in_stock; }
    public void setIn_stock(Boolean in_stock) { this.in_stock = in_stock; }
    
    public Optional<tags> getTag() { return this.tag; }
    public void setTag(Optional<tags> tag) { this.tag = tag; }

    public static Product deserialize(String json) throws Exception {
        ObjectMapper objectMapper = new ObjectMapper();
        return objectMapper.readValue(json, Product.class);
    }

    public String serialize() throws Exception {
        ObjectMapper objectMapper = new ObjectMapper();
        return objectMapper.writeValueAsString(this);
    }

    public enum tags { ELECTRONICS, CLOTHING, FOOD };
}
