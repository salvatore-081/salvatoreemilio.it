package models

import (
	"encoding/json"
	"io/ioutil"
)

type Config struct {
	Port      string          `json:"port"`
	LogLevel  string          `json:"logLevel"`
	RethinkDB RethinkDBConfig `json:"rethinkDB"`
}

type RethinkDBConfig struct {
	Host     string         `json:"host"`
	Port     string         `json:"port"`
	Database DatabaseConfig `json:"database"`
}

type DatabaseConfig struct {
	Name   string                 `json:"name"`
	Tables map[string]TableConfig `json:"tables"`
}

type TableConfig struct {
	Name           string `json:"name"`
	PrimaryKey     string `json:"primaryKey"`
	SecondaryIndex string `json:"secondaryIndex"`
}

func (c *Config) New(path string) error {
	f, e := ioutil.ReadFile(path)
	if e != nil {
		return e
	}

	e = json.Unmarshal([]byte(f), c)
	return e
}
