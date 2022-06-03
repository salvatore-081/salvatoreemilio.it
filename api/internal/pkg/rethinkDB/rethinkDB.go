package rethinkDB

import (
	"context"
	"fmt"

	"github.com/rs/zerolog/log"
	"github.com/salvatore.081/salvatoreemilio-it/models"
	"golang.org/x/sync/errgroup"
	r "gopkg.in/rethinkdb/rethinkdb-go.v6"
)

type RethinkDB struct {
	session *r.Session
	config  models.RethinkDBConfig
}

func (rdb *RethinkDB) NewSession(config models.RethinkDBConfig) (e error) {
	rdb.config = config

	log.Info().Msg(fmt.Sprintf("establishing database connection at %s:%s", config.Host, config.Port))

	r.SetTags("json")

	rdb.session, e = r.Connect(r.ConnectOpts{
		Address:  config.Host + ":" + config.Port,
		Database: config.Database.Name,
	})
	if e != nil {
		return e
	}

	log.Info().Msg("database connection established")

	c, e := r.DBList().Run(rdb.session)
	if e != nil {
		return e
	}

	dbList := []string{}

	e = c.All(&dbList)
	if e != nil {
		return e
	}

	dbCheck := false

	for _, db := range dbList {
		if db == config.Database.Name {
			dbCheck = true
			break
		}
	}

	g, _ := errgroup.WithContext(context.TODO())

	if !dbCheck {
		log.Info().Msg(fmt.Sprintf("missing database '%s'", config.Database.Name))

		_, e := r.DBCreate(config.Database.Name).RunWrite(rdb.session)
		if e != nil {
			return e
		}
		log.Info().Msg(fmt.Sprintf("database %s created", config.Database.Name))

		for _, table := range config.Database.Tables {
			table := table
			g.Go(func() error {
				return rdb.createTable(table)
			})
		}
	} else {
		c, e := r.TableList().Run(rdb.session)
		if e != nil {
			return e
		}

		tableList := []string{}

		e = c.All(&tableList)
		if e != nil {
			return e
		}

		for _, table := range config.Database.Tables {
			table := table

			g.Go(func() error {
				check := false

				for _, t := range tableList {
					if t == table.Name {
						check = true
						c, e = r.Table(table.Name).Info().Run(rdb.session)
						if e != nil {
							return e
						}

						result := []models.TableInfo{}

						e = c.All(&result)
						if e != nil {
							return e
						}

						existingPrimaryKey := result[0].PrimaryKey

						if existingPrimaryKey != table.PrimaryKey {

							log.Warn().Msg(fmt.Sprintf("primary key mismatch for table %s", table.Name))

							_, e = r.Table(table.Name).Config().Update(map[string]string{
								"name": "_" + table.Name,
							}).Run(rdb.session)
							if e != nil {
								return e
							}

							e = rdb.createTable(table)
							if e != nil {
								return e
							}

							primaryKey := "id"

							if len(table.PrimaryKey) > 0 {
								primaryKey = table.PrimaryKey
							}

							_, e = r.Table(table.Name).Insert(r.Table("_" + table.Name).Map(func(row r.Term) interface{} {
								return row.Merge(map[string]interface{}{
									primaryKey: row.Field(existingPrimaryKey),
								})
							})).Run(rdb.session)

							if e != nil {
								return e
							}
						}
						break
					}
				}

				if !check {
					log.Info().Msg(fmt.Sprintf("table '%s' is missing", table.Name))

					if e = rdb.createTable(table); e == nil {
						log.Info().Msg(fmt.Sprintf("table '%s' created", table.Name))
					}

					return e
				} else {
					secondaryIndexes, e := rdb.listTableSecondaryIndex(table)
					if e != nil {
						return e
					}

					secondaryIndexCheck := false

					for _, secondaryIndex := range secondaryIndexes {
						if secondaryIndex == table.SecondaryIndex {
							secondaryIndexCheck = true
						} else {
							log.Warn().Msg(fmt.Sprintf("dropping unused secondary index '%s' for table '%s'", secondaryIndex, table.Name))
							e = rdb.dropSecondaryIndex(table, secondaryIndex)
							if e != nil {
								return e
							}
						}
					}

					if len(table.SecondaryIndex) == 0 {
						secondaryIndexCheck = true
					}

					if !secondaryIndexCheck {
						log.Warn().Msg(fmt.Sprintf("creating secondary index '%s' for table %s", table.SecondaryIndex, table.Name))
						e = rdb.createSecondaryIndex(table)
						if e != nil {
							return e
						}
					}
				}
				return nil
			})
		}
	}

	return g.Wait()
}

func (rdb *RethinkDB) createTable(table models.TableConfig) error {
	_, e := r.TableCreate(table.Name, r.TableCreateOpts{PrimaryKey: table.PrimaryKey}).RunWrite(rdb.session)
	if e != nil {
		return e
	}

	if len(table.SecondaryIndex) > 0 {
		return rdb.createSecondaryIndex(table)
	}

	return nil
}

func (rdb *RethinkDB) listTableSecondaryIndex(table models.TableConfig) ([]string, error) {
	c, e := r.Table(table.Name).IndexList().Run(rdb.session)
	if e != nil {
		return nil, e
	}
	var indexList []string

	e = c.All(&indexList)

	return indexList, e
}

func (rdb *RethinkDB) createSecondaryIndex(table models.TableConfig) (e error) {
	_, e = r.Table(table.Name).IndexCreate(table.SecondaryIndex).Run(rdb.session)
	if e != nil {
		return e
	}

	_, e = r.Table(table.Name).IndexWait(table.SecondaryIndex).Run(rdb.session)
	return e
}

func (rdb *RethinkDB) dropSecondaryIndex(table models.TableConfig, secondaryIndex string) (e error) {
	_, e = r.Table(table.Name).IndexDrop(secondaryIndex).Run(rdb.session)
	return e
}
