.PHONY: up down reset seed logs dev-web install integrations integration-odoo integration-erpnext integration-ifc integration-all integration-logs integration-test

# Core services
up:
	docker compose -f infra/docker-compose.yml up -d --build

down:
	docker compose -f infra/docker-compose.yml down

reset:
	docker compose -f infra/docker-compose.yml down -v

seed:
	@echo "Seeding database schema..."
	docker compose -f infra/docker-compose.yml exec -T db psql -U eagle -d eagle < infra/db/schema.sql
	@echo "Seeding regional factors..."
	docker compose -f infra/docker-compose.yml exec -T db psql -U eagle -d eagle < infra/seeds/regional_factors.csv
	@echo "Seeding spec tier bundles..."
	docker compose -f infra/docker-compose.yml exec -T db psql -U eagle -d eagle < infra/seeds/spec_tier_bundles.sql
	@echo "Seeding trade base..."
	docker compose -f infra/docker-compose.yml exec api python /app/seed_tradebase.py
	@echo "Database seeded successfully!"

logs:
	docker compose -f infra/docker-compose.yml logs -f

dev-web:
	cd apps/web && npm run dev

install:
	cd apps/web && npm install
	cd services/api && pip install -r requirements.txt
	cd services/parser && pip install -r requirements.txt
	cd services/rules && pip install -r requirements.txt
	cd services/pricing && pip install -r requirements.txt
	cd services/reports && pip install -r requirements.txt

# Integration services
integration-odoo:
	@echo "Starting Odoo + Connector..."
	cd integrations/odoo && docker-compose up -d
	@echo "Odoo: http://localhost:8069"
	@echo "Connector: http://localhost:5002"

integration-ifc:
	@echo "Starting IfcOpenShell QTO service..."
	docker compose -f infra/docker-compose.yml up -d ifcopenshell
	@echo "IFC QTO: http://localhost:5001"

integration-all:
	@echo "Starting all integration services..."
	$(MAKE) integration-odoo
	$(MAKE) integration-ifc
	@echo "All integrations ready!"
	@echo "  - Odoo: http://localhost:8069"
	@echo "  - Odoo Connector: http://localhost:5002"
	@echo "  - IFC QTO: http://localhost:5001"

integration-logs:
	@echo "Tailing integration service logs..."
	docker logs -f eagle-odoo-connector 2>&1 | sed 's/^/[odoo-connector] /' &
	docker logs -f eagle-ifcopenshell 2>&1 | sed 's/^/[ifcopenshell] /'

integration-test:
	@echo "Testing Odoo connector health..."
	curl -s http://localhost:5002/health | python -m json.tool
	@echo ""
	@echo "Testing IFC QTO service health..."
	curl -s http://localhost:5001/health | python -m json.tool

integration-down:
	@echo "Stopping integration services..."
	cd integrations/odoo && docker-compose down
	docker compose -f infra/docker-compose.yml stop ifcopenshell odoo-connector

# Combined workflows
all: up integration-all seed
	@echo "Eagle Eye + Integrations ready!"
	@echo "  - API: http://localhost:8000/docs"
	@echo "  - Web: http://localhost:3000"
	@echo "  - n8n: http://localhost:5678"
	@echo "  - Odoo: http://localhost:8069"
	@echo "  - IFC QTO: http://localhost:5001"

help:
	@echo "Eagle Eye Makefile Commands:"
	@echo ""
	@echo "Core Services:"
	@echo "  make up              - Start Eagle Eye core services"
	@echo "  make down            - Stop all services"
	@echo "  make reset           - Reset (delete volumes)"
	@echo "  make seed            - Seed database with schema + data"
	@echo "  make logs            - Tail service logs"
	@echo ""
	@echo "Development:"
	@echo "  make dev-web         - Start Next.js dev server"
	@echo "  make install         - Install dependencies"
	@echo ""
	@echo "Integrations:"
	@echo "  make integration-odoo      - Start Odoo + connector"
	@echo "  make integration-ifc       - Start IfcOpenShell QTO"
	@echo "  make integration-all       - Start all integrations"
	@echo "  make integration-logs      - Tail integration logs"
	@echo "  make integration-test      - Test integration health"
	@echo "  make integration-down      - Stop integrations"
	@echo ""
	@echo "Workflows:"
	@echo "  make all             - Start everything (core + integrations)"
	@echo ""
	@echo "For ERPNext setup, see: integrations/erpnext/README.md"

