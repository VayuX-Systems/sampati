#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Sampati local development startup script
# Usage: ./scripts/dev.sh [up|down|logs|reset]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
COMPOSE_FILE="${PROJECT_ROOT}/deploy/docker-compose.yml"
ENV_FILE="${PROJECT_ROOT}/.env"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() { echo -e "${BLUE}[INFO]${NC} $*"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $*"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }

check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    if ! docker compose version &> /dev/null; then
        log_error "Docker Compose is not available. Please install Docker Compose."
        exit 1
    fi
}

create_env_file() {
    if [[ ! -f "${ENV_FILE}" ]]; then
        log_info "Creating .env file from template..."
        cat > "${ENV_FILE}" << 'ENVEOF'
# Sampati Development Environment
# Copy this file to .env and modify as needed

SAMPATI_ENV=dev
SAMPATI_BASE_URL=http://localhost:8000
SAMPATI_DATABASE_URL=postgresql+asyncpg://sampati:sampati-dev@localhost:5432/sampati
SAMPATI_REDIS_URL=redis://localhost:6379/0
SAMPATI_STORAGE_URL=http://localhost:9000
SAMPATI_STORAGE_BUCKET=sampati-evidence
SAMPATI_KEY_MODE=local
SAMPATI_OIDC_ISSUER=
SAMPATI_OIDC_CLIENT_ID=
SAMPATI_OIDC_CLIENT_SECRET=
SAMPATI_SMTP_URL=
SAMPATI_DEFAULT_LOCALE=en-IN
SAMPATI_TIMEZONE=Asia/Kolkata
SAMPATI_PLUGIN_SANDBOX=container
SAMPATI_AI_ENABLED=false
SAMPATI_AI_BASE_URL=
SAMPATI_LOG_LEVEL=debug
SAMPATI_SECRET_KEY=dev-secret-key-change-in-production
ENVEOF
        log_success "Created .env file. Please review and modify as needed."
    fi
}

cmd_up() {
    check_docker
    create_env_file
    log_info "Starting Sampati development environment..."
    docker compose -f "${COMPOSE_FILE}" up -d
    log_success "Services started!"
    log_info "API: http://localhost:8000"
    log_info "API Docs: http://localhost:8000/docs"
    log_info "MinIO Console: http://localhost:9001 (sampati / sampati-dev)"
    log_info "Mailcatcher: http://localhost:1080"
    log_info "PostgreSQL: localhost:5432 (sampati / sampati-dev)"
    log_info "Redis: localhost:6379"
}

cmd_down() {
    check_docker
    log_info "Stopping Sampati development environment..."
    docker compose -f "${COMPOSE_FILE}" down
    log_success "Services stopped!"
}

cmd_logs() {
    check_docker
    docker compose -f "${COMPOSE_FILE}" logs -f "${@:2}"
}

cmd_reset() {
    check_docker
    log_warn "This will destroy all data! Are you sure? (y/N)"
    read -r confirm
    if [[ "${confirm}" =~ ^[Yy]$ ]]; then
        docker compose -f "${COMPOSE_FILE}" down -v
        log_success "Environment reset complete!"
    else
        log_info "Reset cancelled."
    fi
}

cmd_status() {
    check_docker
    docker compose -f "${COMPOSE_FILE}" ps
}

main() {
    case "${1:-up}" in
        up)
            cmd_up
            ;;
        down)
            cmd_down
            ;;
        logs)
            cmd_logs "$@"
            ;;
        reset)
            cmd_reset
            ;;
        status)
            cmd_status
            ;;
        *)
            echo "Usage: $0 {up|down|logs|reset|status}"
            exit 1
            ;;
    esac
}

main "$@"
