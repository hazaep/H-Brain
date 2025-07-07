#!/bin/bash
# init.sh - Crear nuevo proyecto local y subirlo a GitHub

BASE_DIR="$HOME/proyectos/GitSyncCli"
LOG_FILE="$BASE_DIR/git_sync.log"
source "$BASE_DIR/utils/helpers.sh"

echo -e "\n🚀 ${CYAN}GitSyncCli: Crear nuevo repositorio desde cero${RESET}"

read -p "📁 Nombre del directorio del proyecto: " project_dir
project_path="$PWD/$project_dir"

# Crear directorio
mkdir -p "$project_path"
cd "$project_path" || exit 1

# Inicializar repo
git init
log_action "📁 Proyecto inicializado: $project_dir"

# Crear README inicial
echo "# $project_dir" > README.md
echo "Proyecto creado con GitSyncCli 🚀" >> README.md

# Primer commit
git add .
git commit -m "🎉 Proyecto inicial"

# Crear repo remoto en GitHub (usa nombre del folder)
read -p "🌐 ¿Repositorio público? (y/n): " is_public
visibility="private"
[[ "$is_public" == "y" || "$is_public" == "Y" ]] && visibility="public"

read -p "📝 Descripción del repositorio: " description

gh repo create "$project_dir" --$visibility --description "$description" --source=. --remote=origin --push
log_action "🌐 Repo GitHub creado: $project_dir ($visibility)"

echo -e "\n✅ ${GREEN}Proyecto '$project_dir' creado y subido a GitHub exitosamente.${RESET}"
