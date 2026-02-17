# pydigidoc

Python bindings for [libdigidocpp](https://github.com/open-eid/libdigidocpp) via SWIG. Produces installable wheels for creating, validating, and handling digitally signed documents (ASiC-E, BDOC, etc).

## Architecture

- `libdigidocpp/` — upstream C++ library as a git submodule (pinned to v4.3.0)
- `CMakeLists.txt` — builds upstream statically, then builds SWIG Python module
- `swig/pydigidoc.i` — thin wrapper: `%rename` for snake_case + `%include "libdigidocpp.i"`
- `src/pydigidoc/__init__.py` — re-exports SWIG symbols, wraps `initialize()` to use bundled schema files
- Schema files are bundled in the wheel under `pydigidoc/schema/`

## Key decisions

- **Static linking** (`BUILD_SHARED_LIBS=OFF`) — self-contained wheels, LGPL-2.1 compliance via RELINKING.md + sdist source
- **`ANDROID=TRUE` hack** in CMake — skips upstream `install(EXPORT)` which fails with static builds
- **Symlinks** (`etc/`, `cmake/`) created at configure time — upstream uses `CMAKE_SOURCE_DIR` which points to our root, not the submodule
- **SWIG `%rename` before `%include`** — order matters, upstream `.i` declares `%module(directors="1") digidoc`
- **`MACOSX_DEPLOYMENT_TARGET=15.0`** — required by Homebrew OpenSSL 3

## Test

```bash
uv sync --dev
uv run pytest tests/ -v
```

## Build

```bash
# System deps (Ubuntu): libssl-dev libxml2-dev zlib1g-dev libxmlsec1-dev
uv build --wheel
```

Uses scikit-build-core as the build backend bridging CMake. Requires C++23, SWIG 4.0+, CMake 3.20+.

## Git

Never use `git -C <path>` — always run git commands from the working directory.

## CI

`.github/workflows/build.yml` — 4 jobs:
1. `build` — every push, Ubuntu only
2. `build_wheels` — on release, cibuildwheel v3.3.1 across Linux/macOS/Windows
3. `build_sdist` — on release
4. `publish` — OIDC trusted publishing to PyPI

Linux wheels build OpenSSL and xmlsec1 from source inside manylinux_2_28 with GCC 13.

## Version management

`bump-my-version` configured in pyproject.toml. Updates version in pyproject.toml, `__init__.py`, and CMakeLists.txt, commits, and tags.
