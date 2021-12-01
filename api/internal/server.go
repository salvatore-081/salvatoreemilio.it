package main

import (
	"fmt"
	"net/http"
	"os"
	"strings"

	"github.com/99designs/gqlgen/graphql/handler"
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/httplog"

	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
	"github.com/salvatore.081/salvatoreemilio-it-internal-api/graph"
	"github.com/salvatore.081/salvatoreemilio-it-internal-api/pkg/rethinkdb"

	"github.com/salvatore.081/salvatoreemilio-it-internal-api/graph/generated"
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

	// SERVER
	srv := handler.NewDefaultServer(generated.NewExecutableSchema(generated.Config{Resolvers: &graph.Resolver{
		DB: &rethinkdb,
	}}))

	router := chi.NewRouter()
	router.Use(httplog.RequestLogger(log.Logger))

	// router.Handle("/graphql", playground.Handler("GraphQL Playground", "/"))

	log.Info().Msg("salvatoreemilio.it internal API listening on port " + port)
	router.Handle("/", srv)

	log.Fatal().Err(http.ListenAndServe(":"+port, router)).Msg("")
}
