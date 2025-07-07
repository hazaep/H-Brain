#!/bin/bash
# feature.sh - Crear una nueva rama de feature y (opcional) una PR en GitHub

BASE_DIR="$HOME/proyectos/GitSyncCli"
LOG_FILE="$BASE_DIR/git_sync.log"
source "$BASE_DIR/utils/helpers.sh"

echo -e "\n🌿 ${CYAN}GitSyncCli: Crear nueva rama de feature${RESET}"
check_git_repo || exit 1
check_gh_auth

read -p "🧩 Nombre de la nueva funcionalidad (snake_case o-kebab): " feature_name
branch_name="feature/${feature_name}"

# Crear y cambiar a la nueva rama
git checkout -b "$branch_name"
log_action "🌿 Nueva rama creada: $branch_name"

echo -e "${GREEN}✅ Rama '$branch_name' creada y activada.${RESET}"

# Push inicial
git push -u origin "$branch_name"
log_action "🚀 Rama '$branch_name' publicada en remoto"

# Preguntar si deseas crear PR
read -p "🔁 ¿Crear Pull Request ahora? (y/n): " create_pr
if [[ "$create_pr" == "y" || "$create_pr" == "Y" ]]; then
  read -p "📝 Título de la PR: " pr_title
  read -p "📋 Descripción (puedes dejar en blanco): " pr_desc
  read -p "📄 ¿PR como borrador (draft)? (y/n): " is_draft

  draft_flag=""
  [[ "$is_draft" == "y" || "$is_draft" == "Y" ]] && draft_flag="--draft"

  gh pr create --title "$pr_title" --body "$pr_desc" --base main --head "$branch_name" $draft_flag
  log_action "🔁 PR creada desde $branch_name → main"
fi

echo -e "\n✅ ${GREEN}Flujo de feature completado.${RESET}"
