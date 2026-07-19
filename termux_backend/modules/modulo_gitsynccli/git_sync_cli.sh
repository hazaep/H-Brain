#!/data/data/com.termux/files/usr/bin/bash
# git_sync_cli.sh con integración de gh

set -e

GREEN="\e[32m"
RED="\e[31m"
YELLOW="\e[33m"
CYAN="\e[36m"
RESET="\e[0m"

clear
printf "${CYAN}🔁 Git Sync CLI - H-Brain 🧠${RESET}\n"
echo "----------------------------------------"

# Verifica si estamos dentro de un repo Git
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo -e "${RED}❌ Este directorio no es un repositorio Git.${RESET}"
  exit 1
fi

# Verifica si `gh` está instalado
if ! command -v gh &> /dev/null; then
  echo -e "${YELLOW}⚠️ GitHub CLI (gh) no está instalado. Algunas funciones no estarán disponibles.${RESET}"
  GH_AVAILABLE=false
else
  GH_AVAILABLE=true
fi

# Mostrar rama actual
branch=$(git rev-parse --abbrev-ref HEAD)
user=$(git config user.name)
echo -e "${GREEN}✔️  Rama actual:${RESET} $branch  | Usuario Git: ${CYAN}$user${RESET}"
git status -s

# Función: detectar si hubo cambios en GitHub Web (rama remota adelantada)
check_for_remote_commits() {
  git fetch origin "$branch" >/dev/null 2>&1
  remote_commits=$(git log HEAD..origin/$branch --oneline)

  if [[ -n "$remote_commits" ]]; then
    echo -e "${YELLOW}⚠️  Esta rama tiene commits en GitHub que aún no están en tu máquina.${RESET}"
    echo -e "${CYAN}📦 Commits detectados en GitHub remoto:${RESET}"
    echo "$remote_commits"
    echo -e "${YELLOW}🛑 Recomendación: haz 'git pull --rebase' antes de continuar.${RESET}\n"
  fi
}

# Función para registrar logs
log_action() {
  local accion="$1"
  local fecha=$(date +"%Y-%m-%d %H:%M:%S")
  echo "[$fecha] ($user) [$branch] $accion" >> git_sync.log
}

echo -e "\n${YELLOW}¿Qué acción deseas realizar?${RESET}"
echo "  1) git pull --rebase"
echo "  2) git add . + commit"
echo "  3) git push"
echo "  4) git log --oneline"
echo "  5) git diff"
echo "  6) git checkout <rama>"
echo "  7) Crear nueva rama"
echo "  8) Sincronizar completo (pull → commit → push)"
echo "  9) gh auth status"
echo " 10) gh pr create (Pull Request)"
echo " 11) gh repo view"
echo " 12) gh gist create desde archivo"
echo " 13) Salir"
read -p "Selecciona una opción [1-13]: " opcion

case $opcion in
  1)
    git pull --rebase origin "$branch"
    log_action "pull --rebase"
    ;;
  2)
    check_for_remote_commits
    read -p "Mensaje de commit: " mensaje
    git add .
    git commit -m "$mensaje"
    log_action "commit: $mensaje"
    ;;
  3)
    check_for_remote_commits
    git push origin "$branch"
    log_action "push"
    ;;
  4)
    git log --oneline --graph --decorate -n 10
    log_action "ver log"
    ;;
  5)
    git diff
    log_action "ver diff"
    ;;
  6)
    read -p "Nombre de la rama: " target_branch
    git checkout "$target_branch"
    log_action "checkout $target_branch"
    ;;
  7)
    read -p "Nombre de nueva rama: " new_branch
    git checkout -b "$new_branch"
    log_action "crear rama $new_branch"
    ;;
  8)
    check_for_remote_commits
    read -p "Mensaje de commit: " mensaje
    git pull --rebase origin "$branch"
    git add .
    git commit -m "$mensaje"
    git push origin "$branch"
    log_action "sync completo: $mensaje"
    ;;
  9)
    if [ "$GH_AVAILABLE" = true ]; then
      gh auth status
      log_action "gh auth status"
    else
      echo -e "${RED}❌ gh no está disponible.${RESET}"
    fi
    ;;
  10)
    if [ "$GH_AVAILABLE" = true ]; then
      read -p "Título del PR: " titulo
      read -p "Descripción del PR: " desc
      gh pr create --title "$titulo" --body "$desc"
      log_action "crear PR: $titulo"
    else
      echo -e "${RED}❌ gh no está disponible.${RESET}"
    fi
    ;;
  11)
    if [ "$GH_AVAILABLE" = true ]; then
      gh repo view --web
      log_action "ver repo"
    else
      echo -e "${RED}❌ gh no está disponible.${RESET}"
    fi
    ;;
  12)
    if [ "$GH_AVAILABLE" = true ]; then
      read -p "Archivo a subir como Gist: " file
      read -p "Descripción: " desc
      gh gist create "$file" --public --desc "$desc"
      log_action "crear gist: $file"
    else
      echo -e "${RED}❌ gh no está disponible.${RESET}"
    fi
    ;;
  13)
    echo -e "${CYAN}👋 Saliendo...${RESET}"
    log_action "salir"
    exit 0
    ;;
  *)
    echo -e "${RED}❌ Opción inválida${RESET}"
    ;;
esac

echo -e "\n${GREEN}✅ Acción completada.${RESET}"
