FROM gcc:latest

RUN apt-get update && apt-get install -y \
    nlohmann-json3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY *.cpp *.h ./

# 使用更可靠的方法找到 json.hpp
RUN JSON_INCLUDE_PATH=$(find /usr/include -name "json.hpp" | xargs dirname) \
    && g++ -std=c++17 -o app app.cpp TestRunner.cpp Logger.cpp -I${JSON_INCLUDE_PATH} -ldl -I/usr/include

CMD ["./app"]