#!/bin/bash

CYAN="\e[36m"
GREEN="\e[32m"
YELLOW="\e[33m"
RED="\e[31m"
RESET="\e[0m"

log_action() {
  local mensaje="$1"
  local fecha=$(date +"%Y-%m-%d %H:%M:%S")
  echo "[$fecha] $mensaje" >> "$HOME/proyectos/GitSyncCli/git_sync.log"
}

check_git_repo() {
  if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo -e "${RED}❌ Este directorio no es un repositorio Git.${RESET}"
    return 1
  fi
  return 0
}

check_gh_auth() {
  if command -v gh &> /dev/null; then
    gh auth status > /dev/null 2>&1 || echo -e "${YELLOW}⚠️ No estás autenticado en GitHub.${RESET}"
  fi
}

check_for_remote_commits() {
  local branch="$1"
  git fetch origin "$branch" >/dev/null 2>&1
  local remote_commits=$(git log HEAD..origin/$branch --oneline)

  if [[ -n "$remote_commits" ]]; then
    echo -e "${YELLOW}⚠️ Esta rama tiene commits remotos no aplicados localmente:${RESET}"
    echo "$remote_commits"
    echo -e "${YELLOW}🛑 Se recomienda hacer 'git pull --rebase' antes de continuar.${RESET}\n"
  fi
}
