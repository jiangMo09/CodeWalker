import com.google.gson.Gson;
import java.util.*;

public class Logger {
    private static List<Map<String, Object>> testCases = new ArrayList<>();
    private static int totalCorrect = 0;
    private static int totalTestcases = 0;

    public static void logTestCase(int index, TestRunner.TestCaseStats stats, List<Object> inputs, Object expectedOutput) {
        totalTestcases++;
        if (stats.passed) totalCorrect++;

        Map<String, Object> testCaseResult = new HashMap<>();
        testCaseResult.put("test_case", index);
        testCaseResult.put("passed", stats.passed);
        testCaseResult.put("inputs", new Gson().toJson(inputs));
        testCaseResult.put("output", stats.result == null ? "undefined" : new Gson().toJson(stats.result));
        testCaseResult.put("expected", new Gson().toJson(expectedOutput));
        testCaseResult.put("run_time", String.format("%.3f ms", stats.runTime));
        testCaseResult.put("memory", String.format("%.3f KB", stats.memoryUsed));

        testCases.add(testCaseResult);
    }

    public static void logSummary(TestRunner.Stats stats) {
        Map<String, Object> summary = new HashMap<>();
        summary.put("run_result", testCases);
        summary.put("total_correct", totalCorrect);
        summary.put("total_testcases", totalTestcases);
        summary.put("total_run_time", String.format("%.3f ms", stats.totalRunTime));
        summary.put("total_run_memory", String.format("%.3f MB", stats.totalMemoryUsed / 1024));
        summary.put("all_passed", stats.allTestsPassed);

        System.out.println(new Gson().toJson(summary));
    }
}