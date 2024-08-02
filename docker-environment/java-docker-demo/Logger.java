import com.google.gson.Gson;

public class Logger {
    public static void logTestCase(int index, TestRunner.TestCaseStats stats, Object[] inputs, Object expectedOutput) {
    System.out.printf("Test case %d: %s. Inputs: %s. Output: %s. Expected: %s%n", 
                      index, stats.passed ? "Passed" : "Failed", formatInputs(inputs), formatOutput(stats.result), formatOutput(expectedOutput));
    System.out.printf("Run time: %.3f ms%n", stats.runTime / 1_000_000.0);
    System.out.printf("Memory used: %.3f KB%n", stats.memoryUsed / 1024.0);
    if (stats.error != null) {
        System.out.printf("Error: %s%n", stats.error);
    }
}

    public static void logSummary(TestRunner.Stats stats) {
        System.out.println(stats.allTestsPassed ? "All test cases passed!" : "Some test cases failed.");
        System.out.printf("Total run time: %.3f ms%n", stats.totalRunTime / 1_000_000.0);
        System.out.printf("Total memory used: %.3f KB%n", stats.totalMemoryUsed / 1024.0);
    }
}