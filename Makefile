# Makefile for Spacecraft Scheduler Configuration

SERVICE := spacecraft_scheduler

.PHONY: help build up down clean setup-dirs jupyter setup shell run exec logs ps restart rebuild

help:
	@echo "Spacecraft Scheduler - Commands:"
	@echo "  build     Build image"
	@echo "  up        Start services (detached)"
	@echo "  down      Stop services"
	@echo "  clean     Stop and remove volumes/orphans"
	@echo "  shell     Open an interactive shell (see below)"
	@echo "  run       One-off shell (new container, removed on exit)"
	@echo "  exec      Shell into the running container"
	@echo "  logs      Tail logs"
	@echo "  ps        Show compose status"
	@echo "  restart   Restart the service"
	@echo "  rebuild   Rebuild image then up"
	@echo "  jupyter   Print Jupyter URL hint"

# Use compose v2 CLI
COMPOSE := docker compose

build:
	$(COMPOSE) build

up: setup-dirs
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

clean:
	$(COMPOSE) down -v --remove-orphans
	docker system prune -f

# Interactive shells
# 'run' starts a *new* container with your compose config and drops you into bash.
# --service-ports maps the ports as declared in compose (useful if you want Jupyter accessible)
run:
	$(COMPOSE) run --rm --service-ports $(SERVICE) bash

# 'exec' opens a shell *in the running container* (start with `make up` first)
exec:
	$(COMPOSE) exec $(SERVICE) bash

# Friendly alias: try exec if running, else fall back to run
shell:
	@if $(COMPOSE) ps --status=running --services | grep -q '^$(SERVICE)$$'; then \
		echo ">> Attaching shell to running $(SERVICE)"; \
		$(COMPOSE) exec $(SERVICE) bash; \
	else \
		echo ">> No running $(SERVICE); starting one-off shell..."; \
		$(COMPOSE) run --rm --service-ports $(SERVICE) bash; \
	fi

logs:
	$(COMPOSE) logs -f $(SERVICE)

ps:
	$(COMPOSE) ps

restart:
	$(COMPOSE) restart $(SERVICE)

rebuild:
	$(COMPOSE) build --no-cache
	$(COMPOSE) up -d

# Data/results directories
setup-dirs:
	mkdir -p data results logs

# Dev info
jupyter:
	@echo "Jupyter Lab: http://localhost:8888"
	@echo "Code in container: /app/spacecraft_scheduler"
