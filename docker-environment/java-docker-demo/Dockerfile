FROM openjdk:20-slim

WORKDIR /app

RUN apt-get update && apt-get install -y wget
RUN wget https://repo1.maven.org/maven2/com/google/code/gson/gson/2.10.1/gson-2.10.1.jar

COPY TestRunner.java .
COPY Logger.java .
COPY App.java .

RUN javac -cp gson-2.10.1.jar *.java

ENV NODE_ENV=production

CMD ["java", "-cp", ".:gson-2.10.1.jar", "App"]