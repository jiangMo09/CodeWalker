FROM openjdk:17-slim

# 安裝必要的工具
RUN apt-get update && apt-get install -y wget

WORKDIR /app

# 下載 Gson
RUN wget https://repo1.maven.org/maven2/com/google/code/gson/gson/2.10.1/gson-2.10.1.jar

# 複製所有 Java 文件
COPY *.java .

# 編譯所有 Java 文件
RUN javac -cp gson-2.10.1.jar *.java

# 設置運行命令
CMD ["java", "-cp", ".:gson-2.10.1.jar", "App"]