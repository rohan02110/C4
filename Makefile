.PHONY: help build up down restart reset-ring7 logs test ui

help:
	@echo "Chakravyuha: The Seventh Ring — Operational Makefile"
	@echo "====================================================="
	@echo "  make build         - Build all 7 ring containers & scoring engine"
	@echo "  make up            - Launch isolated challenge environment"
	@echo "  make down          - Stop and clean up containers"
	@echo "  make reset-ring7   - Respawn Ring 7 pwn container for clean state"
	@echo "  make test          - Run automated smoke tests & end-to-end solver"
	@echo "  make ui            - Start Vite development server for Battlefield Portal UI"

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

reset-ring7:
	docker compose restart antahkaranam

logs:
	docker compose logs -f

test:
	python tests/full_chain_e2e.py

ui:
	cd ui && npm run dev
