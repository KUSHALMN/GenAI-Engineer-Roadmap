package Month07.Day23;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;

/**
 * Custom Testing Framework Mock:
 * Re-creates JUnit-style test execution, assertions, and test outcome reporting.
 */
public class JUnitTestingFrameworkMock {

    public interface TestCase {
        void run() throws Exception;
    }

    public static class TestRunner {
        private int passed = 0;
        private int failed = 0;

        public void runTest(String testName, TestCase test) {
            try {
                test.run();
                passed++;
            } catch (Throwable t) {
                failed++;
                System.err.println("Test " + testName + " failed: " + t.getMessage());
            }
        }

        public int getPassed() { return passed; }
        public int getFailed() { return failed; }
    }

    public static void main(String[] args) {
        TestRunner runner = new TestRunner();
        runner.runTest("testSuccess", () -> { assert 1 + 1 == 2; });
        runner.runTest("testFailure", () -> { throw new AssertionError("Expected 5 got 4"); });

        assert runner.getPassed() == 1;
        assert runner.getFailed() == 1;
        System.out.println("Day 23 JUnit Testing Framework verification passed.");
    }
}
