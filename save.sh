#!/bin/sh
# save.sh: one time-stamped save of everything in this folder.
#
#   ./save.sh "what changed"
#
# Each save can be gone back to. To see every save with its time:
#   git log --format='%ad  %h  %s' --date=format:'%b %d %H:%M:%S'
#
# Bench runs, test spirals and Python's cache are not part of a save
# (.gitignore). They stay on the drive where they are.
cd "$(dirname "$0")" || exit 1
what="${1:-save}"
[ $# -gt 0 ] && shift
git add -A || exit 1
if git diff --cached --quiet; then
    echo "nothing new to save at $(date '+%H:%M:%S')"
    exit 0
fi
if [ $# -gt 0 ]; then
    credit=$(printf '%s\n' "$@")
    git commit -q -m "$what" -m "$credit" || exit 1
else
    git commit -q -m "$what" || exit 1
fi
git log -1 --format='saved %ad  %h  %s' --date=format:'%H:%M:%S'
