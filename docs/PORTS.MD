## METRICS AND LOGS
- PORTAINER: 11990, 11991  ```./.env```
- GRAFANA: 11000 ```./.env```
- LOKI: 11010  ```./grafana/loki/config.yaml ./grafana/promtail/config.yaml ```
- PROMTAIL: 11020  ```./grafana/promtail/config.yaml```
- NODE-EXPORTER: 11030  ```./.env ./prometheus/config.yaml```
- PROMETHEUS: 11040  ```./.env```
- CADVISOR: 11050  ```./.env ./prometheus/config.yaml```
## AUTHENTICATION
- KEYCLOAK: 12000  ```./.env```
## DATABASE
- POSTGRES: 13010 ```./.env```
- RETHINKDB_DRIVER: 13020 ```./rethinkdb/rethinkdb.conf```
- RETHINKDB_CLUSTER: 13021  ```./rethinkdb/rethinkdb.conf```
## API
- GRAPHQL_SERVER: 14010 ```./.env```
## WEBSERVER
- NGINX: 15000  ```./.env ./nginx/conf.d/default.conf```

