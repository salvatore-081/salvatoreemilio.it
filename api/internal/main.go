package main

import (
	"fmt"
	"net"
	"os"
	"strings"

	grpczerolog "github.com/grpc-ecosystem/go-grpc-middleware/providers/zerolog/v2"
	middleware "github.com/grpc-ecosystem/go-grpc-middleware/v2"
	"github.com/grpc-ecosystem/go-grpc-middleware/v2/interceptors/logging"
	"github.com/grpc-ecosystem/go-grpc-middleware/v2/interceptors/tags"
	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
	"github.com/salvatore.081/salvatoreemilio-it/pkg/rethinkdb"
	"github.com/salvatore.081/salvatoreemilio-it/proto"
	"github.com/salvatore.081/salvatoreemilio-it/resolvers"
	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"
)

func main() {

	// LOGGER
	envLogLevel := strings.ToLower(os.Getenv("LOG_LEVEL"))
	logLevel, e := zerolog.ParseLevel(envLogLevel)
	if e != nil {
		logLevel = 0
	}
	if envLogLevel == "" {
		logLevel = 0
	}

	zerolog.SetGlobalLevel(logLevel)

	logOutput := zerolog.ConsoleWriter{Out: os.Stdout}
	logOutput.FormatLevel = func(i interface{}) string {
		return strings.ToUpper(fmt.Sprintf("|%s|", i))
	}

	logOutput.FormatTimestamp = func(i interface{}) string {
		return ""
	}

	log.Logger = zerolog.New(logOutput)
	if e != nil {
		log.Info().Err(e).Msg(fmt.Sprintf("Unknown LOG_LEVEL: %s, defaulting to DEBUG", os.Getenv("LOG_LEVEL")))
	}
	if envLogLevel == "" {
		log.Info().Msg("Missing LOG_LEVEL, defaulting to DEBUG")
	}

	// PORT
	port := os.Getenv("PORT")
	if len(port) == 0 {
		log.Info().Msg("PORT is not set, defaulting to 14010")
		port = "14010"
	}

	// DEPENDECIES
	var rethinkdb rethinkdb.RethinkDB
	e = rethinkdb.NewSession()
	if e != nil {
		log.Fatal().Err(e).Msg("")
	}

	l, e := net.Listen("tcp", ":"+port)
	if e != nil {
		log.Fatal().Err(e).Msg("Failed to listen for tcp on " + port)
	}

	s := grpc.NewServer(
		middleware.WithUnaryServerChain(
			tags.UnaryServerInterceptor(),
			logging.UnaryServerInterceptor(grpczerolog.InterceptorLogger(log.Logger)),
		),
		middleware.WithStreamServerChain(
			tags.StreamServerInterceptor(),
			logging.StreamServerInterceptor(grpczerolog.InterceptorLogger(log.Logger)),
		))

	server := resolvers.Server{Db: &rethinkdb}

	proto.RegisterInternalServer(s, &server)

	reflection.Register(s)

	log.Info().Msg(fmt.Sprintf("Server listening at %v", l.Addr()))

	if e = s.Serve(l); e != nil {
		log.Fatal().Err(e).Msg("Failed to serve")
	}
}
