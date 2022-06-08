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
	"github.com/salvatore.081/salvatoreemilio-it/models"
	"github.com/salvatore.081/salvatoreemilio-it/pkg/rethinkDB"
	"github.com/salvatore.081/salvatoreemilio-it/proto"
	"github.com/salvatore.081/salvatoreemilio-it/resolvers"
	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"
)

func main() {

	logOutput := zerolog.ConsoleWriter{Out: os.Stdout}
	logOutput.FormatLevel = func(i interface{}) string {
		return strings.ToUpper(fmt.Sprintf("|%s|", i))
	}

	logOutput.FormatTimestamp = func(i interface{}) string {
		return ""
	}

	log.Logger = zerolog.New(logOutput)

	log.Info().Msg("startup")

	log.Info().Msg("loading configuration")

	var config models.Config
	e := config.New("./config.json")
	if e != nil {
		log.Fatal().Err(e).Msg("")
	}

	log.Info().Msg("configuration loaded")

	// LOGGER
	var logLevel zerolog.Level = 0

	if len(config.LogLevel) < 1 {
		log.Info().Msg("missing logLevel, defaulting to DEBUG")
	} else {
		logLevel, e = zerolog.ParseLevel(strings.ToLower(config.LogLevel))
		if e != nil {
			log.Info().Err(e).Msg(fmt.Sprintf("unknown logLevel: %s, defaulting to DEBUG", config.LogLevel))
			logLevel = 0
		}
	}

	zerolog.SetGlobalLevel(logLevel)

	// PORT
	port := config.Port
	if len(port) == 0 {
		log.Info().Msg("port is not set, defaulting to 14010")
		port = "14010"
	}

	// DEPENDECIES
	var rethinkdb rethinkDB.RethinkDB
	e = rethinkdb.NewSession(config.RethinkDB)
	if e != nil {
		log.Fatal().Err(e).Msg("")
	}

	l, e := net.Listen("tcp", ":"+port)
	if e != nil {
		log.Fatal().Err(e).Msg("failed to listen for tcp on " + port)
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

	log.Info().Msg(fmt.Sprintf("server listening at %v", l.Addr()))

	if e = s.Serve(l); e != nil {
		log.Fatal().Err(e).Msg("failed to serve")
	}
}
