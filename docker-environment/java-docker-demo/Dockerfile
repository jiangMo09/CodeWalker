FROM openjdk:11-jdk

WORKDIR /app

COPY App.java .

RUN javac -cp /usr/lib/jvm/java-11-openjdk-amd64/lib/tools.jar App.java

CMD ["java", "-cp", ".:/usr/lib/jvm/java-11-openjdk-amd64/lib/tools.jar", "App"]