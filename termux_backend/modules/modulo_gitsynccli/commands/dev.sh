#!/bin/bash
# Flujo de desarrollo: pull → commit → push (extendido con detección de conflictos)

BASE_DIR="$HOME/proyectos/GitSyncCli"
LOG_FILE="$BASE_DIR/git_sync.log"
source "$BASE_DIR/utils/helpers.sh"

echo -e "\n🔁 ${CYAN}GitSyncCli: Flujo de Desarrollo (extendido)${RESET}"
check_git_repo || exit 1
check_gh_auth

branch=$(git rev-parse --abbrev-ref HEAD)
user=$(git config user.name)
repo=$(basename -s .git `git config --get remote.origin.url`)

log_action "🔧 Inicio flujo dev en rama '$branch' para '$repo'"

# Verifica cambios remotos
check_for_remote_commits "$branch"

# Pull con rebase
echo -e "\n📥 Haciendo pull --rebase desde 'origin/$branch'..."
if ! git pull --rebase origin "$branch"; then
  echo -e "${RED}❌ Rebase fallido. Se detectaron conflictos.${RESET}"

  # Mostrar conflictos
  echo -e "\n🧨 Archivos en conflicto:"
  git diff --name-only --diff-filter=U

  echo -e "${YELLOW}\n🛠️  Tienes 3 opciones:${RESET}"
  echo "  1) Ver conflictos (abrir en editor o revisar manualmente)"
  echo "  2) Abortar rebase"
  echo "  3) Salir sin cambios"

  read -p "Selecciona una opción [1-3]: " conflict_option

  case "$conflict_option" in
    1)
      echo -e "${YELLOW}⚠️ Abre los archivos con conflicto, resuélvelos y luego ejecuta:${RESET}"
      echo "   git add <archivo_resuelto>"
      echo "   git rebase --continue"
      echo -e "${CYAN}Luego vuelve a ejecutar 'gsync dev' para continuar.${RESET}"
      log_action "⚠️ Rebase detenido por conflicto. Esperando resolución manual."
      exit 0
      ;;
    2)
      git rebase --abort
      echo -e "${GREEN}✅ Rebase abortado.${RESET}"
      log_action "❌ Rebase abortado por usuario debido a conflictos"
      exit 1
      ;;
    3)
      echo -e "${RED}⏹️ Salida sin resolver conflictos.${RESET}"
      log_action "❌ Rebase cancelado sin resolver conflictos"
      exit 1
      ;;
    *)
      echo -e "${RED}❌ Opción inválida.${RESET}"
      exit 1
      ;;
  esac
fi

log_action "📥 git pull --rebase origin/$branch"

# Mostrar cambios locales
echo -e "\n📦 Cambios detectados localmente:"
git status -s

# Preguntar por mensaje de commit
read -p "📝 Mensaje para el commit: " mensaje

# Commit + push
echo -e "\n🧼 Agregando archivos, haciendo commit y push..."
git add .
git commit -m "$mensaje"
log_action "📝 Commit: $mensaje"

git push origin "$branch"
log_action "📤 Push a origin/$branch"

echo -e "\n✅ ${GREEN}Flujo de desarrollo completado correctamente.${RESET}"

# Preguntar si se desea crear PR al terminar dev
read -p "🔁 ¿Crear PR para esta rama? (y/n): " crear_pr
if [[ "$crear_pr" == "y" || "$crear_pr" == "Y" ]]; then
  read -p "📝 Título de la PR: " pr_title
  read -p "📋 Descripción: " pr_desc
  gh pr create --title "$pr_title" --body "$pr_desc" --base main --head "$branch"
  log_action "🔁 PR creada desde rama '$branch'"
  echo -e "${GREEN}✅ Pull Request creada.${RESET}"
fi
