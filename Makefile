-include ./.env
export

ARGS = $(filter-out $@,$(MAKECMDGOALS))

up:
ifeq ($(wildcard .env),)
	$(MAKE) init
	docker compose up -d
	$(MAKE) airflow-init
	$(MAKE) migrate-up
endif
	docker compose up -d

stop:
	docker compose stop

# completely removes all project data from
destroy:
	docker compose down -v --rmi all --remove-orphans
	rm -f ./docker-compose.yml ./.env

# to run the project for the first time
# currently, there is only one environment - dev
init:
	cp ./docker/dev/docker-compose.yml ./docker-compose.yml
	cp ./env/.env.dev ./.env

# technical command for airflow initialization
airflow-init:
	docker compose run --rm airflow airflow db upgrade
	docker compose run --rm airflow airflow users create \
		--username ${AIRFLOW_ADMIN_USER} \
		--password ${AIRFLOW_ADMIN_PASSWORD} \
		--firstname Air \
		--lastname Flow \
		--role Admin \
		--email ${AIRFLOW_ADMIN_EMAIL}

# command to install new python packages
poentry:
	docker compose exec airflow poetry $(CMD)

# performs migrations for ClickHouse, from the src/migrations/clickhouse folder
migrate-up:
	@until docker compose exec -T clickhouse clickhouse-client --query "SELECT 1" >/dev/null 2>&1; do \
		sleep 2; \
	done
	for file in src/migrations/clickhouse/*.sql; do \
		echo "Applying $$file"; \
		docker compose exec -T clickhouse clickhouse-client \
			--host=$(CLICKHOUSE_HOST) \
			--port=$(CLICKHOUSE_PORT) \
			--user=$(CLICKHOUSE_USER) \
			--password=$(CLICKHOUSE_PASSWORD) \
			--multiquery < $$file; \
	done

# the command executes an SQL query and displays the resulting rates in the console
check-rates:
	docker compose exec -T clickhouse clickhouse-client \
		--database=nbu \
		--query="SELECT * FROM rates"
