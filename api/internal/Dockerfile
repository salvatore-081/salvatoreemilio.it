FROM golang:latest AS builder

WORKDIR /app

COPY . .

RUN go mod download

RUN CGO_ENABLED=0 go build -o /internal-api

FROM scratch

COPY --from=builder /internal-api /app/internal-api

WORKDIR /app

ENTRYPOINT ["/app/internal-api"]