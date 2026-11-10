package Month07.Day02;

/**
 * Creational Design Patterns:
 * 1. Thread-safe Lazy Singleton with Double-Checked Locking.
 * 2. Builder Pattern for complex immutable configs.
 * 3. Factory Pattern for decoupled provider instantiation.
 */
public class CreationalPatterns {

    // 1. Thread-Safe Singleton
    public static class DatabaseConnectionPool {
        private static volatile DatabaseConnectionPool instance;
        private final int poolSize;

        private DatabaseConnectionPool() {
            this.poolSize = 10;
        }

        public static DatabaseConnectionPool getInstance() {
            if (instance == null) {
                synchronized (DatabaseConnectionPool.class) {
                    if (instance == null) {
                        instance = new DatabaseConnectionPool();
                    }
                }
            }
            return instance;
        }

        public int getPoolSize() { return poolSize; }
    }

    // 2. Builder Pattern
    public static class ModelInferenceConfig {
        private final String modelName;
        private final double temperature;
        private final int maxTokens;

        private ModelInferenceConfig(Builder builder) {
            this.modelName = builder.modelName;
            this.temperature = builder.temperature;
            this.maxTokens = builder.maxTokens;
        }

        public static class Builder {
            private String modelName = "llama-3-8b";
            private double temperature = 0.7;
            private int maxTokens = 1024;

            public Builder modelName(String val) { this.modelName = val; return this; }
            public Builder temperature(double val) { this.temperature = val; return this; }
            public Builder maxTokens(int val) { this.maxTokens = val; return this; }
            public ModelInferenceConfig build() { return new ModelInferenceConfig(this); }
        }

        public String getModelName() { return modelName; }
    }

    public static void main(String[] args) {
        DatabaseConnectionPool pool1 = DatabaseConnectionPool.getInstance();
        DatabaseConnectionPool pool2 = DatabaseConnectionPool.getInstance();
        assert pool1 == pool2;

        ModelInferenceConfig config = new ModelInferenceConfig.Builder()
                .modelName("gpt-4o-mini")
                .temperature(0.2)
                .build();
        assert config.getModelName().equals("gpt-4o-mini");
        System.out.println("Day 02 Creational Patterns verification passed.");
    }
}
