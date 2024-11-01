#!/bin/bash

# === 🔧 CONFIG ===
export GIT_AUTHOR_NAME="Jagrat Sharma"
export GIT_COMMITTER_NAME="Jagrat Sharma"
export GIT_AUTHOR_EMAIL="jagrat.sharma@torontomu.ca"
export GIT_COMMITTER_EMAIL="$GIT_AUTHOR_EMAIL"

START_DATE="2024-11-01"
END_DATE="2025-02-28"
BRANCH="master"

FILES=("src/assistant.py" "src/ui.py" "src/logic.py" "README.md" "docs/changelog.md" "docs/notes.md")
MESSAGES=("Refactor UI" "Add command handler" "Update docstring" "Adjust speech engine" "Tweak response layout" "Fix minor bug")

# === ✅ Setup ===
mkdir -p src docs
echo "# Voice Assistant Project" > README.md
echo "# Change Log" > docs/changelog.md
echo "# Dev Notes" > docs/notes.md
echo "#!/usr/bin/env python3\n# assistant.py" > src/assistant.py
echo "# ui.py for GUI layout" > src/ui.py
echo "# logic.py for command handling" > src/logic.py

git add .
git commit -m "Project initialized" --date="$START_DATE"
git push -u origin $BRANCH --force

# === 🧠 Loop over date range ===
current_date="$START_DATE"
skip_until=""

while [[ "$current_date" < "$END_DATE" ]]; do
  # Insert random break every 10-15 days
  if [[ -z "$skip_until" && $((RANDOM % 11)) -eq 0 ]]; then
    skip_length=$((5 + RANDOM % 6))
    skip_until=$(date -I -d "$current_date + $skip_length days")
    echo "⏸️ Break from $current_date to $skip_until"
  fi

  if [[ -n "$skip_until" && "$current_date" < "$skip_until" ]]; then
    current_date=$(date -I -d "$current_date + 1 day")
    continue
  else
    skip_until=""
  fi

  # Commit 1–3 times per day
  commits=$((1 + RANDOM % 3))
  for ((i=0; i<$commits; i++)); do
    FILE=${FILES[$RANDOM % ${#FILES[@]}]}
    MSG=${MESSAGES[$RANDOM % ${#MESSAGES[@]}]}
    echo "# $MSG on $current_date" >> "$FILE"
    git add "$FILE"
    COMMIT_TIME="$current_date 12:0$i:00"
    GIT_AUTHOR_DATE="$COMMIT_TIME" GIT_COMMITTER_DATE="$COMMIT_TIME" \
    git commit -m "$MSG ($current_date)"
  done

  current_date=$(date -I -d "$current_date + 1 day")
done

# Final push
git push origin $BRANCH --force
echo "✅ Fake commit history complete with realistic file changes!"
