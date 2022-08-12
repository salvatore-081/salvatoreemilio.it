FROM golang:latest AS builder

WORKDIR /app

COPY . .

RUN go mod download

RUN CGO_ENABLED=0 go build -o /backup

FROM scratch

COPY --from=builder /backup /app/backup

WORKDIR /app

ENTRYPOINT ["/app/backup"]

