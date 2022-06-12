package models

import (
	"github.com/salvatore.081/salvatoreemilio-it/proto"
)

type TableInfo struct {
	Db                DBInfo   `json:"db"`
	DocCountEstimates []int64  `json:"doc_count_estimates"`
	Id                string   `json:"id"`
	Indexes           []string `json:"indexes"`
	Name              string   `json:"name"`
	PrimaryKey        string   `json:"primary_key"`
	Type              string   `json:"type"`
}

type DBInfo struct {
	Id   string `json:"id"`
	Name string `json:"name"`
	Type string `json:"type"`
}

type WatchFeed[T proto.Project | proto.User] struct {
	NewVal *T `json:"new_val,omitempty"`
	OldVal *T `json:"old_val,omitempty"`
}
