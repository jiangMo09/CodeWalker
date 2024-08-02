public static Stats runTests(String typedCode, String functionName, String[] inputs, String[] expectedOutputs, int parametersCount) throws Exception {
    Class<?> solutionClass = compileAndLoadSolution(typedCode);
    
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
    stats.testCaseResults = new TestCaseStats[inputs.length / parametersCount];

    for (int i = 0; i < inputs.length; i += parametersCount) {
        TestCaseStats testCaseStats = new TestCaseStats();
        stats.testCaseResults[i / parametersCount] = testCaseStats;

        try {
            Object[] params = parseInputs(Arrays.copyOfRange(inputs, i, i + parametersCount), method.getParameterTypes());
            Object expectedOutput = parseValue(expectedOutputs[i / parametersCount], method.getReturnType());

            long startTime = System.nanoTime();
            long startMemory = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();

            Object result = method.invoke(instance, params);

            long endTime = System.nanoTime();
            long endMemory = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();

            testCaseStats.runTime = endTime - startTime;
            testCaseStats.memoryUsed = endMemory - startMemory;
            testCaseStats.result = result;
            testCaseStats.passed = compareResults(result, expectedOutput);

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

private static Object[] parseInputs(String[] inputs, Class<?>[] parameterTypes) {
    Object[] params = new Object[inputs.length];
    for (int i = 0; i < inputs.length; i++) {
        params[i] = parseValue(inputs[i], parameterTypes[i]);
    }
    return params;
}

private static Object parseValue(String value, Class<?> type) {
    if (type.isArray()) {
        return parseArray(value, type.getComponentType());
    } else if (List.class.isAssignableFrom(type)) {
        return parseList(value);
    } else if (type == int.class || type == Integer.class) {
        return Integer.parseInt(value);
    } else if (type == long.class || type == Long.class) {
        return Long.parseLong(value);
    } else if (type == double.class || type == Double.class) {
        return Double.parseDouble(value);
    } else if (type == boolean.class || type == Boolean.class) {
        return Boolean.parseBoolean(value);
    } else if (type == char.class || type == Character.class) {
        return value.charAt(0);
    } else if (type == String.class) {
        return value;
    }
    throw new IllegalArgumentException("Unsupported type: " + type);
}

private static Object parseArray(String value, Class<?> componentType) {
    String[] elements = value.substring(1, value.length() - 1).split(",");
    Object array = Array.newInstance(componentType, elements.length);
    for (int i = 0; i < elements.length; i++) {
        Array.set(array, i, parseValue(elements[i].trim(), componentType));
    }
    return array;
}

private static List<Object> parseList(String value) {
    String[] elements = value.substring(1, value.length() - 1).split(",");
    List<Object> list = new ArrayList<>();
    for (String element : elements) {
        list.add(parseValue(element.trim(), Object.class));
    }
    return list;
}

private static boolean compareResults(Object result, Object expectedOutput) {
    if (result == null && expectedOutput == null) {
        return true;
    }
    if (result == null || expectedOutput == null) {
        return false;
    }
    if (result.getClass().isArray() && expectedOutput.getClass().isArray()) {
        return Arrays.deepEquals((Object[]) result, (Object[]) expectedOutput);
    }
    return result.equals(expectedOutput);
}