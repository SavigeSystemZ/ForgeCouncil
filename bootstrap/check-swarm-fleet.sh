#!/usr/bin/env bash
# AIAST Swarm Fleet: Health & Integrity Check
# Verifies that all agent hooks, anti-drift rules, and swarm tools are present and aligned.

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=bootstrap/lib/aiaast-lib.sh
source "${SCRIPT_DIR}/lib/aiaast-lib.sh"

TARGET_REPO="${1:-$(pwd)}"

log_info() { echo "✅ [SWARM CHECK] $1"; }
log_fail() { echo "❌ [SWARM FAIL] $1"; exit 1; }
log_warn() { echo "⚠️ [SWARM WARN] $1"; }

REPO_MODE="$(aiaast_detect_repo_mode "${TARGET_REPO}")"

check_file() {
    local rel="$1"
    if [[ "${REPO_MODE}" == "template" ]]; then
        if [[ ! -f "${TARGET_REPO}/${rel}" ]]; then
            log_fail "Missing critical swarm file: ${rel}"
        fi
    else
        local installed_rel="${rel#TEMPLATE/}"
        if [[ ! -f "${TARGET_REPO}/${installed_rel}" ]]; then
            log_fail "Missing critical swarm file: ${installed_rel}"
        fi
    fi
}

check_symlink() {
    local rel="$1"
    if [[ "${REPO_MODE}" == "template" ]]; then
        # In template source, these are real files, not symlinks.
        return 0
    fi
    if [[ ! -L "${TARGET_REPO}/${rel}" ]]; then
        log_warn "Missing or broken symlink: ${rel}. Attempting repair..."
        return 1
    fi
}

log_info "Verifying Swarm Fleet Core Tools..."
check_file "bootstrap/git-swarm-manager.sh"
check_file "bootstrap/sync-agent-adapters.sh"
check_file "bootstrap/repair-swarm-integrity.sh"
check_file "_system/MCP_CONFIG.md"
check_file "_system/AUTH_RECOVERY_PROTOCOL.md"
check_file "_system/mcp/MCP_SURVIVAL_PLAYBOOK.md"

log_info "Verifying Anti-Drift Rules..."
check_file ".cursor/rules/00-anti-drift-ssot.mdc"

log_info "Verifying Agent Adapters..."
check_file ".cursorrules"
check_file ".windsurfrules"
check_file ".clinerules"
check_file ".continuerules"

log_info "Verifying Copilot Symlink..."
if ! check_symlink ".github/copilot-instructions.md"; then
    mkdir -p "${TARGET_REPO}/.github"
    ln -sf "../TEMPLATE/.github/copilot-instructions.md" "${TARGET_REPO}/.github/copilot-instructions.md"
    log_info "Repaired Copilot symlink."
fi

log_info "Verifying SSH Identity for 'whyte'..."
if [[ "$(whoami)" != "whyte" ]]; then
    log_warn "Current user is $(whoami), expected 'whyte' for swarm operations."
fi

echo "swarm_fleet_ok"
exit 0
