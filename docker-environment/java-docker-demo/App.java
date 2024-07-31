import javax.tools.*;
import java.io.*;
import java.lang.reflect.*;
import java.net.*;
import java.util.*;

public class App {
    public static void main(String[] args) throws Exception {
        String functionCode = System.getenv("GREET_FUNCTION");
        if (functionCode == null || functionCode.isEmpty()) {
            throw new IllegalArgumentException("GREET_FUNCTION environment variable is not set or is empty");
        }

        String fullClassCode = "public class DynamicGreeter { public static String greet() { " + functionCode + " } }";

        // 編譯動態生成的類
        JavaCompiler compiler = ToolProvider.getSystemJavaCompiler();
        DiagnosticCollector<JavaFileObject> diagnostics = new DiagnosticCollector<>();
        JavaFileObject file = new JavaSourceFromString("DynamicGreeter", fullClassCode);
        Iterable<? extends JavaFileObject> compilationUnits = Arrays.asList(file);
        JavaCompiler.CompilationTask task = compiler.getTask(null, null, diagnostics, null, null, compilationUnits);

        boolean success = task.call();
        if (!success) {
            for (Diagnostic diagnostic : diagnostics.getDiagnostics()) {
                System.err.format("Error on line %d: %s%n", diagnostic.getLineNumber(), diagnostic.getMessage(null));
            }
            System.exit(1);
        }

        // 加載並執行動態生成的類
        URLClassLoader classLoader = URLClassLoader.newInstance(new URL[] { new File(".").toURI().toURL() });
        Class<?> cls = Class.forName("DynamicGreeter", true, classLoader);
        Method greetMethod = cls.getMethod("greet");

        // 測量執行時間和記憶體使用
        long startTime = System.nanoTime();
        long startMemory = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();

        String result = (String) greetMethod.invoke(null);

        long endTime = System.nanoTime();
        long endMemory = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();

        double runTime = (endTime - startTime) / 1e6; // 轉換為毫秒
        long memoryUsed = endMemory - startMemory;

        System.out.println("Function result: " + result);
        System.out.printf("Run time: %.3f ms%n", runTime);
        System.out.printf("Memory used: %.3f KB%n", memoryUsed / 1024.0);
    }
}

class JavaSourceFromString extends SimpleJavaFileObject {
    final String code;

    JavaSourceFromString(String name, String code) {
        super(URI.create("string:///" + name.replace('.', '/') + Kind.SOURCE.extension), Kind.SOURCE);
        this.code = code;
    }

    @Override
    public CharSequence getCharContent(boolean ignoreEncodingErrors) {
        return code;
    }
}