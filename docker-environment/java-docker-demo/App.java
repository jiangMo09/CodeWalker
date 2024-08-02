import com.google.gson.Gson;

public class App {
    public static void main(String[] args) {
        try {
            String dataInput = System.getenv("DATA_INPUT");
            if (dataInput == null) {
                throw new RuntimeException("DATA_INPUT environment variable is not set");
            }

            Gson gson = new Gson();
            TestData testData = gson.fromJson(dataInput, TestData.class);

            String[] inputs = testData.data_input.split("\n");
            String[] expectedOutputs = testData.correct_answer.split("\n");

            TestRunner.Stats stats = TestRunner.runTests(testData.typed_code, testData.function_name, inputs, expectedOutputs, testData.parameters_count);

            for (int i = 0; i < stats.testCaseResults.length; i++) {
                Logger.logTestCase(i + 1, stats.testCaseResults[i], new Object[]{inputs[i]}, expectedOutputs[i]);
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
}