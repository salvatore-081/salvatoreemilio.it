FROM golang:latest

WORKDIR /app

COPY . ./

RUN go mod download

RUN go build -o /internal-api

CMD ["/internal-api"]

