#!/bin/bash
docker-compose -f traefik/compose.yaml down
docker-compose -f frontend/compose.yaml down
docker-compose -f api/public/compose.yaml down
docker-compose -f api/internal/compose.yaml down
docker-compose -f db/rethinkdb/compose.yaml down
docker-compose -f iam/keycloak/compose.yaml down
docker-compose -f cloud/nextcloud/compose.yaml down
docker-compose -f tools/portainer/compose.yaml down
docker-compose -f tools/grafana/compose.yaml down
docker-compose -f tools/metrics/prometheus/compose.yaml down
docker-compose -f tools/logs/loki/compose.yaml down


