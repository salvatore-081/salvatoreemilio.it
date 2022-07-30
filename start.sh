#!/bin/bash
docker-compose -f tools/logs/loki/compose.yaml up -d
docker-compose -f traefik/compose.yaml up -d
docker-compose -f iam/keycloak/compose.yaml up -d
docker-compose -f tools/portainer/compose.yaml up -d
docker-compose -f tools/metrics/prometheus/compose.yaml up -d
docker-compose -f tools/grafana/compose.yaml up -d
docker-compose -f db/rethinkdb/compose.yaml up -d
docker-compose -f api/internal/compose.yaml up -d
docker-compose -f api/public/compose.yaml up -d
docker-compose -f frontend/compose.yaml up -d
docker-compose -f cloud/nextcloud/compose.yaml up -d
