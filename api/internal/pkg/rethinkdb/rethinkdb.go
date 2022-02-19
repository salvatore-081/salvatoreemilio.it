package rethinkdb

import (
	"errors"
	"fmt"
	"os"

	"github.com/rs/zerolog/log"
	r "gopkg.in/rethinkdb/rethinkdb-go.v6"
)

type RethinkDB struct {
	session *r.Session
}

const defaultTable = "users"
const primaryKey = "email"

func (rdb *RethinkDB) NewSession() (e error) {
	r.SetTags("json")

	a := os.Getenv("DB_HOST") + ":" + os.Getenv("DB_PORT")
	log.Info().Msg(fmt.Sprintf("establishing database connection at %s", a))

	db := os.Getenv("DB_DATABASE")
	if db == "" {
		return errors.New("environment variable DB_DATABASE not set")
	}

	s, e := r.Connect(r.ConnectOpts{
		Address: a,
	})
	if e != nil {
		return e
	}

	c, e := r.DBList().Run(s)
	if e != nil {
		return e
	}

	dbList := []string{}

	e = c.All(&dbList)
	if e != nil {
		return e
	}

	dbCheck := false

	for _, v := range dbList {
		if v == db {
			dbCheck = true
			break
		}
	}

	if !dbCheck {
		log.Info().Msg(fmt.Sprintf("database '%s' is missing, a new one will be created", db))

		_, e := r.DBCreate(db).RunWrite(s)
		if e != nil {
			return e
		}

		e = createDefaultTable(db, s)
		if e != nil {
			return e
		}

		log.Info().Msg(fmt.Sprintf("database '%s' created with default table '%s'", db, defaultTable))
	} else {
		c, e := r.DB(db).TableList().Run(s)
		if e != nil {
			return e
		}

		tableList := []string{}

		e = c.All(&tableList)
		if e != nil {
			return e
		}

		tableCheck := false

		for _, t := range tableList {
			if t == defaultTable {
				tableCheck = true
				r.DB(db).TableList()
				break
			}
		}

		if !tableCheck {
			log.Info().Msg(fmt.Sprintf("default table '%s' is missing", defaultTable))

			e = createDefaultTable(db, s)
			if e != nil {
				return e
			}

			log.Info().Msg(fmt.Sprintf("default table '%s' created", defaultTable))
		}
	}

	_ = s.Close()

	rdb.session, e = r.Connect(r.ConnectOpts{
		Address:  a,
		Database: db,
	})
	if e != nil {
		return e
	}

	return nil
}

func createDefaultTable(db string, s *r.Session) error {
	_, e := r.DB(db).TableCreate(defaultTable, r.TableCreateOpts{PrimaryKey: primaryKey}).RunWrite(s)
	if e != nil {
		return e
	}
	return nil
}
