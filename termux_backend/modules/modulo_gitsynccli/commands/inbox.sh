#!/bin/bash
# inbox.sh - Bandeja de entrada GitHub: PRs, Issues, Notificaciones

BASE_DIR="$HOME/proyectos/GitSyncCli"
LOG_FILE="$BASE_DIR/git_sync.log"
source "$BASE_DIR/utils/helpers.sh"

echo -e "\n📬 ${CYAN}GitSyncCli: Bandeja de Entrada${RESET}"
check_git_repo || exit 1
check_gh_auth

repo=$(basename -s .git `git config --get remote.origin.url`)
branch=$(git rev-parse --abbrev-ref HEAD)

log_action "📬 Consultando bandeja de entrada en repo '$repo'"

echo -e "\n🧠 ${YELLOW}Estado actual:${RESET}"
echo "📁 Proyecto: $repo"
echo "🌿 Rama actual: $branch"
echo "🔧 Último commit local:"
git log -1 --pretty=format:"%h %s (%cr)"

# Mostrar PRs asignadas
echo -e "\n🔁 ${CYAN}Pull Requests asignadas a ti:${RESET}"
gh pr list --assignee @me --state open --limit 5 --json number,title,updatedAt --template '{{range .}}{{printf "#%v" .number}} {{.title}} (⏱ {{.updatedAt}}){{"\n"}}{{end}}' || echo "❌ No se pudo obtener PRs."

# Mostrar Issues asignados
echo -e "\n📝 ${CYAN}Issues asignados a ti:${RESET}"
gh issue list --assignee @me --state open --limit 5 --json number,title,updatedAt --template '{{range .}}{{printf "#%v" .number}} {{.title}} (⏱ {{.updatedAt}}){{"\n"}}{{end}}' || echo "❌ No se pudo obtener Issues."

# Mostrar notificaciones
echo -e "\n🔔 ${CYAN}Notificaciones recientes:${RESET}"
gh api notifications --paginate -q '.[] | "\(.repository.full_name): \(.subject.title) [\(.reason)]"' | head -n 5 || echo "❌ No se pudo obtener notificaciones."

echo -e "\n✅ ${GREEN}Fin de la bandeja de entrada.${RESET}"
