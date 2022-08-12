package models

import (
	"encoding/json"
	"io/ioutil"
)

type Config struct {
	LogLevel      string `json:"logLevel"`
	MaxRetention  int16  `json:"max_retention"`
	Time          string `json:"time"`
	MBSizeWarning int32  `json:"mb_size_warning"`
}

func (c *Config) New(path string) error {
	f, e := ioutil.ReadFile(path)
	if e != nil {
		return e
	}

	e = json.Unmarshal([]byte(f), c)
	return e
}
