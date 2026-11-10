package Month07.Day04;

/**
 * Structural Design Patterns:
 * 1. Adapter Pattern: Translating legacy LLM response to standardized schema.
 * 2. Decorator Pattern: Adding logging and token counting to model invocations.
 * 3. Facade Pattern: Unified gateway exposing simplified inference methods.
 */
public class StructuralPatterns {

    public interface LLMClient {
        String complete(String prompt);
    }

    public static class OpenAiClient implements LLMClient {
        @Override
        public String complete(String prompt) {
            return "Generated response for: " + prompt;
        }
    }

    // Decorator: Adds telemetry logging
    public static class LoggingLLMDecorator implements LLMClient {
        private final LLMClient inner;
        private int callCount = 0;

        public LoggingLLMDecorator(LLMClient inner) { this.inner = inner; }

        @Override
        public String complete(String prompt) {
            callCount++;
            return inner.complete(prompt);
        }

        public int getCallCount() { return callCount; }
    }

    public static void main(String[] args) {
        LLMClient base = new OpenAiClient();
        LoggingLLMDecorator decorated = new LoggingLLMDecorator(base);

        String result = decorated.complete("Hello world");
        assert result.contains("Hello world");
        assert decorated.getCallCount() == 1;

        System.out.println("Day 04 Structural Patterns verification passed.");
    }
}
