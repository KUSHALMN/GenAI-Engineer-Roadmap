import java.util.*;

/**
 * Day 07: Immutability & Defensive Copying in Java
 * Implements a thread-safe immutable record ensuring:
 * 1. final class (prevent inheritance)
 * 2. private final fields
 * 3. Deep defensive copies in constructors and getters for mutable collections.
 */
public final class ImmutableClassPattern {

    private final String modelId;
    private final List<String> targetLayers;
    private final Map<String, Double> hyperparameters;

    public ImmutableClassPattern(String modelId, List<String> targetLayers, Map<String, Double> hyperparameters) {
        this.modelId = modelId;
        // Defensive copies
        this.targetLayers = new ArrayList<>(targetLayers);
        this.hyperparameters = new HashMap<>(hyperparameters);
    }

    public String getModelId() { return modelId; }

    public List<String> getTargetLayers() {
        return Collections.unmodifiableList(targetLayers); // Prevent external mutation
    }

    public Map<String, Double> getHyperparameters() {
        return Collections.unmodifiableMap(hyperparameters);
    }

    public static void main(String[] args) {
        List<String> layers = new ArrayList<>(Arrays.asList("q_proj", "v_proj"));
        Map<String, Double> params = new HashMap<>();
        params.put("lr", 0.0002);

        ImmutableClassPattern config = new ImmutableClassPattern("Llama-3", layers, params);

        // Verify that mutating original input collections does not affect the immutable object
        layers.add("k_proj");
        params.put("lr", 0.999);

        assert config.getTargetLayers().size() == 2 : "Immutable object must retain original 2 layers";
        assert config.getHyperparameters().get("lr") == 0.0002 : "Immutable object must retain original lr";

        // Verify unmodifiable getter
        try {
            config.getTargetLayers().add("out_proj");
            assert false : "Should throw UnsupportedOperationException";
        } catch (UnsupportedOperationException e) {
            // Expected
        }

        System.out.println("Day 07 DSA ImmutableClassPattern verification passed!");
    }
}
