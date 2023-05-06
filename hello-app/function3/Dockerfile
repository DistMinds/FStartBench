FROM golang:alpine3.13 AS builder
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
RUN apk update && apk add alpine-sdk git && rm -rf /var/cache/apk/*
RUN go env -w GOPROXY=https://goproxy.cn,direct
# RUN echo '140.82.112.4 github.com' >> /etc/hosts
WORKDIR /usr/src/app

COPY go.mod .
COPY go.sum .
RUN go mod download

COPY server.go .
RUN go build -o ./server ./server.go

FROM alpine:latest

RUN apk update && apk add ca-certificates && rm -rf /var/cache/apk/*

WORKDIR /usr/src/app

COPY --from=builder /usr/src/app/server .

EXPOSE 9000
ENTRYPOINT ["./server"]
