#!/bin/sh
# install_lucent_models.sh: Lucent's three model files for the 3C's eye, pulled from
# GitHub, the canonical, at the commit the eye was read from. Never from a copy on
# a drive. (Everett, 17 Nov 2026: "You only pull from GitHub when you're installing
# something. You don't pull parallel.")
#
#   ./install_lucent_models.sh
#
# Writes organs/lucent/ beside this file (git ignores it: the files are Lucent's,
# and GitHub keeps them). Every file is checked against Lucent's own SHA256SUMS,
# pulled from the same commit; one that does not match stops the install.
set -eu
COMMIT=b582a1df2a309ea1ba821e69ef928f58ea9f2b5e
RAW="https://raw.githubusercontent.com/EverettNC/LUCENT/$COMMIT/public/mediapipe"
HERE="$(cd "$(dirname "$0")" && pwd)"
DEST="$HERE/organs/lucent"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

curl -fsSL "$RAW/SHA256SUMS" -o "$TMP/SHA256SUMS"
for f in face_landmarker.task hand_landmarker.task pose_landmarker_lite.task; do
    curl -fsSL "$RAW/models/$f" -o "$TMP/$f"
    want=$(grep " models/$f\$" "$TMP/SHA256SUMS" | cut -d' ' -f1)
    got=$(shasum -a 256 "$TMP/$f" | cut -d' ' -f1)
    if [ -z "$want" ] || [ "$want" != "$got" ]; then
        echo "stopped: $f from GitHub does not match Lucent's SHA256SUMS at $COMMIT" >&2
        exit 1
    fi
done
mkdir -p "$DEST"
mv "$TMP"/*.task "$DEST/"
echo "$COMMIT" > "$DEST/FROM_LUCENT_COMMIT"
echo "Lucent's models, from GitHub at $COMMIT, checked, in $DEST:"
( cd "$DEST" && shasum -a 256 *.task )
