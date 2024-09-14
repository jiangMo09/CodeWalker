import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.util.*;

public class App {
    public static void main(String[] args) {
        try {
            String dataInput = System.getenv("DATA_INPUT");
            if (dataInput == null) {
                throw new RuntimeException("DATA_INPUT environment variable is not set");
            }

            Gson gson = new Gson();
            TestData testData = gson.fromJson(dataInput, TestData.class);

            List<Object> inputs = parseInput(testData.data_input, testData.parameters_count);
            List<Object> expectedOutputs = parseOutput(testData.correct_answer);

            TestRunner.Stats stats = TestRunner.runTests(testData.typed_code, testData.function_name, inputs, expectedOutputs, testData.parameters_count);

            for (int i = 0; i < stats.testCaseResults.size(); i++) {
                Logger.logTestCase(
                    i + 1,
                    stats.testCaseResults.get(i),
                    inputs.subList(i * testData.parameters_count, (i + 1) * testData.parameters_count),
                    expectedOutputs.get(i)
                );
            }

            Logger.logSummary(stats);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    static class TestData {
        String data_input;
        String correct_answer;
        String function_name;
        int parameters_count;
        String typed_code;
    }

    private static List<Object> parseInput(String input, int parametersCount) {
        List<Object> result = new ArrayList<>();
        String[] lines = input.split("\n");
        for (String line : lines) {
            if (line.startsWith("[") && line.endsWith("]")) {
                // 處理數組輸入
                if (line.contains("\"")) {
                    // 字符串數組
                    result.add(gson.fromJson(line, String[].class));
                } else {
                    // 整數數組
                    result.add(gson.fromJson(line, int[].class));
                }
            } else if (line.startsWith("\"") && line.endsWith("\"")) {
                // 處理字符串輸入
                result.add(line.substring(1, line.length() - 1));
            } else {
                try {
                    // 嘗試解析為整數
                    result.add(Integer.parseInt(line));
                } catch (NumberFormatException e) {
                    // 如果不是整數，則保留為字符串
                    result.add(line);
                }
            }
        }
        return result;
    }

    private static List<Object> parseOutput(String output) {
        List<Object> result = new ArrayList<>();
        String[] lines = output.split("\n");
        for (String line : lines) {
            if (line.equals("true") || line.equals("false")) {
                result.add(Boolean.parseBoolean(line));
            } else if (line.startsWith("[") && line.endsWith("]")) {
                result.add(gson.fromJson(line, int[].class));
            } else if (line.startsWith("\"") && line.endsWith("\"")) {
                result.add(line.substring(1, line.length() - 1));
            } else {
                try {
                    result.add(Integer.parseInt(line));
                } catch (NumberFormatException e) {
                    result.add(line);
                }
            }
        }
        return result;
    }

    private static final Gson gson = new Gson();
}