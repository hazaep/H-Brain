#!/bin/bash
# issue.sh - Crear Issue + rama asociada (y opcionalmente una PR)

BASE_DIR="$HOME/proyectos/GitSyncCli"
LOG_FILE="$BASE_DIR/git_sync.log"
source "$BASE_DIR/utils/helpers.sh"

echo -e "\n📋 ${CYAN}GitSyncCli: Crear Issue + Rama asociada${RESET}"
check_git_repo || exit 1
check_gh_auth

read -p "📝 Título del Issue: " issue_title
read -p "📄 Descripción del Issue (puede estar vacía): " issue_desc

# Crear el issue
issue_output=$(gh issue create --title "$issue_title" --body "$issue_desc" --assignee @me --json number,title,url 2>/dev/null)
if [[ $? -ne 0 ]]; then
  echo -e "${RED}❌ No se pudo crear el Issue.${RESET}"
  exit 1
fi

issue_number=$(echo "$issue_output" | jq -r '.number')
issue_url=$(echo "$issue_output" | jq -r '.url')
branch_name="issue/$(echo "$issue_title" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g' | sed 's/[^a-z0-9_-]//g')"

# Crear la rama y cambiar a ella
git checkout -b "$branch_name"
git push -u origin "$branch_name"

log_action "📋 Issue #$issue_number creado: $issue_title"
log_action "🌿 Rama '$branch_name' creada para el Issue"

echo -e "\n✅ Issue creado: $issue_url"
echo -e "🌿 Nueva rama: ${GREEN}$branch_name${RESET}"

# Preguntar si se desea crear PR desde esta rama
read -p "🔁 ¿Crear PR asociada a este Issue? (y/n): " create_pr
if [[ "$create_pr" == "y" || "$create_pr" == "Y" ]]; then
  gh pr create --title "$issue_title" --body "$issue_desc\n\nCloses #$issue_number" --base main --head "$branch_name"
  log_action "🔁 PR creada para Issue #$issue_number desde $branch_name"
  echo -e "${GREEN}✅ PR creada y enlazada al Issue.${RESET}"
fi
