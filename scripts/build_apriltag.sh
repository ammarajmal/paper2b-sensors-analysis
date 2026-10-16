#!/usr/bin/env bash
# Build the official AprilRobotics AprilTag v3.4.5 with its Python wrapper, for THIS project's venv (Python 3.12).
# Installs under /mnt/space/adev/toolchains/apriltag (not ~/.local). Rerunnable: it rebuilds from a clean checkout.
set -Eeuo pipefail
cd "$(dirname "$0")/.."
REPO_ROOT=$PWD
VERSION=v3.4.5
EXPECTED=94be783                         # commit prefix the tag resolved to (checked below)
BASE=/mnt/space/adev/toolchains/apriltag
SRC=$BASE/src/apriltag-$VERSION
PREFIX=$BASE/${VERSION#v}
PY=$REPO_ROOT/.venv/bin/python

for c in git cmake ninja cc sha256sum ldd; do command -v $c >/dev/null || { echo "missing tool: $c"; exit 1; }; done
[ -x "$PY" ] || { echo "run 'uv sync' first"; exit 1; }
mkdir -p "$BASE/src"

# 1. source, pinned to the tag, commit verified
[ -d "$SRC/.git" ] || git clone https://github.com/AprilRobotics/apriltag.git "$SRC"
git -C "$SRC" fetch --tags --force origin
git -C "$SRC" reset --hard -q && git -C "$SRC" clean -ffdxq
git -C "$SRC" checkout -q --detach "$VERSION"
COMMIT=$(git -C "$SRC" rev-parse HEAD)
[[ "$COMMIT" == $EXPECTED* ]] || { echo "UNEXPECTED commit $COMMIT for $VERSION"; exit 1; }
echo "commit $COMMIT"

# 2. configure / build / install (shared library + Python wrapper; RPATH so no LD_LIBRARY_PATH is needed)
rm -rf "$SRC/build" "$PREFIX"
cmake -S "$SRC" -B "$SRC/build" -GNinja \
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$PREFIX" \
  -DBUILD_SHARED_LIBS=ON -DBUILD_PYTHON_WRAPPER=ON \
  -DPython3_EXECUTABLE="$PY" \
  -DCMAKE_INSTALL_RPATH="$PREFIX/lib" -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON
cmake --build "$SRC/build" --parallel
cmake --install "$SRC/build"

# 3. make the module importable in the project venv (a .pth file, removed with the venv)
MODDIR=$(dirname "$(find "$PREFIX" -name 'apriltag*.so' -path '*python3*' | head -1)")
SITE=$("$PY" -c 'import site; print(site.getsitepackages()[0])')
echo "$MODDIR" > "$SITE/aprilrobotics_apriltag.pth"

# 4. provenance
LIB=$(find "$PREFIX/lib" -name 'libapriltag.so.3.4.5' | head -1)
git -C "$SRC" archive --format=tar -o "$SRC/build/source.tar" "$COMMIT"
mkdir -p config
cat > config/apriltag_build.json <<EOJ
{"repository":"https://github.com/AprilRobotics/apriltag.git","release":"$VERSION","commit":"$COMMIT",
 "source_archive_sha256":"$(sha256sum "$SRC/build/source.tar" | cut -d' ' -f1)",
 "prefix":"$PREFIX","library":"$LIB","library_sha256":"$(sha256sum "$LIB" | cut -d' ' -f1)",
 "python_module_dir":"$MODDIR","python":"$("$PY" -VV | tr '\n' ' ')","compiler":"$(cc --version | head -1)",
 "cmake":"$(cmake --version | head -1)","built_at":"$(date -Is)"}
EOJ
ldd "$MODDIR"/apriltag*.so | grep -i apriltag || true
echo "OK: $PREFIX  (provenance: config/apriltag_build.json)"
