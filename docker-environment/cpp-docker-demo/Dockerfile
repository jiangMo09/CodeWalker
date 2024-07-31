FROM alpine:latest
RUN apk add --no-cache g++ make lua lua-dev

WORKDIR /app
COPY app.cpp .

RUN g++ -std=c++11 -o app app.cpp -llua -ldl

CMD ["./app"]