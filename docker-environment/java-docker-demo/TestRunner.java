import com.google.gson.Gson;
import javax.tools.*;
import java.io.*;
import java.lang.reflect.Method;
import java.net.*;
import java.util.*;

public class TestRunner {
    public static class TestCaseStats {
        public boolean passed;
        public Object result;
        public long runTime;
        public long memoryUsed;
        public String error;
    }

    public static class Stats {
        public boolean allTestsPassed = true;
        public long totalRunTime = 0;
        public long totalMemoryUsed = 0;
        public TestCaseStats[] testCaseResults;
    }

    public static Stats runTests(String typedCode, String functionName, String[] inputs, String[] expectedOutputs, int parametersCount) throws Exception {
        Class<?> solutionClass = compileAndLoadSolution(typedCode);
        
        // 查找所有匹配名稱的方法
        Method[] methods = solutionClass.getDeclaredMethods();
        Method method = null;
        for (Method m : methods) {
            if (m.getName().equals(functionName) && m.getParameterCount() == parametersCount) {
                method = m;
                break;
            }
        }
        
        if (method == null) {
            throw new NoSuchMethodException(functionName);
        }

        Object instance = solutionClass.getDeclaredConstructor().newInstance();

        Stats stats = new Stats();
        stats.testCaseResults = new TestCaseStats[inputs.length];

        for (int i = 0; i < inputs.length; i++) {
            TestCaseStats testCaseStats = new TestCaseStats();
            stats.testCaseResults[i] = testCaseStats;

            try {
                Object[] params = parseInput(inputs[i], parametersCount, method.getParameterTypes());
                Object expectedOutput = parseOutput(expectedOutputs[i]);

                long startTime = System.nanoTime();
                long startMemory = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();

                Object result = method.invoke(instance, params);

                long endTime = System.nanoTime();
                long endMemory = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();

                testCaseStats.runTime = endTime - startTime;
                testCaseStats.memoryUsed = endMemory - startMemory;
                testCaseStats.result = result;
                testCaseStats.passed = result.toString().equals(expectedOutput.toString());

                stats.totalRunTime += testCaseStats.runTime;
                stats.totalMemoryUsed += testCaseStats.memoryUsed;
                stats.allTestsPassed &= testCaseStats.passed;
            } catch (Exception e) {
                testCaseStats.error = e.getMessage();
                testCaseStats.passed = false;
                stats.allTestsPassed = false;
            }
        }

        return stats;
    }

    private static Class<?> compileAndLoadSolution(String typedCode) throws Exception {
        JavaCompiler compiler = ToolProvider.getSystemJavaCompiler();
        StandardJavaFileManager fileManager = compiler.getStandardFileManager(null, null, null);

        String fullCode = "public class Solution { " + typedCode + " }";
        JavaFileObject javaFile = new SimpleJavaFileObject(URI.create("string:///Solution.java"), JavaFileObject.Kind.SOURCE) {
            @Override
            public CharSequence getCharContent(boolean ignoreEncodingErrors) {
                return fullCode;
            }
        };

        Iterable<? extends JavaFileObject> compilationUnits = Arrays.asList(javaFile);
        JavaCompiler.CompilationTask task = compiler.getTask(null, fileManager, null, null, null, compilationUnits);

        boolean success = task.call();
        if (!success) {
            throw new RuntimeException("Compilation failed");
        }

        URLClassLoader classLoader = URLClassLoader.newInstance(new URL[]{new File(".").toURI().toURL()});
        return Class.forName("Solution", true, classLoader);
    }

    private static Object[] parseInput(String input, int parametersCount, Class<?>[] parameterTypes) {
        Object[] params = new Object[parametersCount];
        String[] parts = input.split(",");
        for (int i = 0; i < parametersCount; i++) {
            params[i] = convertToType(parts[i].trim(), parameterTypes[i]);
        }
        return params;
    }

    private static Object parseOutput(String output) {
        return convertToType(output, Object.class);
    }

    private static Object convertToType(String value, Class<?> type) {
        if (type == int.class || type == Integer.class) {
            return Integer.parseInt(value);
        } else if (type == long.class || type == Long.class) {
            return Long.parseLong(value);
        } else if (type == double.class || type == Double.class) {
            return Double.parseDouble(value);
        } else if (type == float.class || type == Float.class) {
            return Float.parseFloat(value);
        } else if (type == boolean.class || type == Boolean.class) {
            return Boolean.parseBoolean(value);
        } else if (type == char.class || type == Character.class) {
            return value.charAt(0);
        } else if (type == String.class || type == Object.class) {
            return value;
        }
        throw new IllegalArgumentException("Unsupported type: " + type);
    }
}