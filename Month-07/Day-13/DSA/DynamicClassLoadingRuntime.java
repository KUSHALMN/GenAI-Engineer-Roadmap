package Month07.Day13;

import java.lang.reflect.Method;

/**
 * Java Class Loading & Runtime Reflection:
 * Inspects classes dynamically and invokes methods via reflection.
 */
public class DynamicClassLoadingRuntime {

    public static class ModelWorkerPlugin {
        public String executeTask(String task) {
            return "Executed: " + task;
        }
    }

    public static String invokeDynamically(Object target, String methodName, String param) throws Exception {
        Method method = target.getClass().getMethod(methodName, String.class);
        return (String) method.invoke(target, param);
    }

    public static void main(String[] args) throws Exception {
        ModelWorkerPlugin plugin = new ModelWorkerPlugin();
        String output = invokeDynamically(plugin, "executeTask", "generate_embeddings");
        assert output.contains("generate_embeddings");

        System.out.println("Day 13 Dynamic Class Loading verification passed: " + output);
    }
}
