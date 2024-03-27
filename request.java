
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.JsonProcessingException;
import java.io.IOException;
import java.util.List;
import java.util.Optional;

public class request {
    private static final ObjectMapper mapper = new ObjectMapper();
    private Optional<Integer> A = Optional.empty();
    private Optional<String> B = Optional.empty();
    private Optional<Float> C = Optional.empty();
    private List<Boolean> D = new ArrayList<>();

    public request() {} // Default constructor

    // Serializes the Java class object into a JSON string
    public String serialize() {
        try {
            return mapper.writeValueAsString(this);
        } catch (JsonProcessingException e) {
            e.printStackTrace();
            return null;
        }
    }

    // Deserializes the JSON string into a Java class object
    public static request deserialize(String jsonStr) {
        try {
            return mapper.readValue(jsonStr, request.class);
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }

    // Getters and Setters
    public Optional<Integer> getA() { return A; }
    public void setA(Optional<Integer> A) { this.A = A; }
    public Optional<String> getB() { return B; }
    public void setB(Optional<String> B) { this.B = B; }
    public Optional<Float> getC() { return C; }
    public void setC(Optional<Float> C) { this.C = C; }
    public List<Boolean> getD() { return D; }
    public void setD(List<Boolean> D) { this.D = D; }
}
