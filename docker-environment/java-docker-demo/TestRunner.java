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
        public double runTime;
        public double memoryUsed;
        public String error;
    }

    public static class Stats {
        public boolean allTestsPassed = true;
        public double totalRunTime = 0;
        public double totalMemoryUsed = 0;
        public List<TestCaseStats> testCaseResults = new ArrayList<>();
    }

    public static Stats runTests(String typedCode, String functionName, List<Object> inputs, List<Object> expectedOutputs, int parametersCount) throws Exception {
        Class<?> solutionClass = compileAndLoadSolution(typedCode);
        Method method = findMethod(solutionClass, functionName, parametersCount);
        Object instance = solutionClass.getDeclaredConstructor().newInstance();

        Stats stats = new Stats();

        for (int i = 0; i < inputs.size(); i += parametersCount) {
            TestCaseStats testCaseStats = new TestCaseStats();
            stats.testCaseResults.add(testCaseStats);

            try {
                List<Object> params = inputs.subList(i, i + parametersCount);
                Object expectedOutput = expectedOutputs.get(i / parametersCount);

                long startTime = System.nanoTime();
                long startMemory = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();

                Object result = method.invoke(instance, params.toArray());

                long endTime = System.nanoTime();
                long endMemory = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();

                testCaseStats.runTime = (endTime - startTime) / 1_000_000.0;
                testCaseStats.memoryUsed = (endMemory - startMemory) / 1024.0;
                testCaseStats.result = result;
                testCaseStats.passed = compareOutputs(result, expectedOutput);

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

        String imports = 
            "import java.util.*;\n" +
            "import java.io.*;\n" +
            "import java.math.*;\n" +
            "import java.lang.*;\n";
        
        String fullCode = imports + typedCode;

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

    private static Method findMethod(Class<?> solutionClass, String functionName, int parametersCount) throws NoSuchMethodException {
        Method[] methods = solutionClass.getDeclaredMethods();
        for (Method m : methods) {
            if (m.getName().equals(functionName) && m.getParameterCount() == parametersCount) {
                return m;
            }
        }
        throw new NoSuchMethodException(functionName);
    }

    private static boolean compareOutputs(Object result, Object expected) {
        if (result == null && expected == null) return true;
        if (result == null || expected == null) return false;
        if (result instanceof int[] && expected instanceof int[]) {
            return Arrays.equals((int[])result, (int[])expected);
        }
        if (result instanceof String[] && expected instanceof String[]) {
            return Arrays.equals((String[])result, (String[])expected);
        }
        return result.toString().equals(expected.toString());
    }
}