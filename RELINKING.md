# Relinking Instructions (LGPL-2.1 Compliance)

pydigidoc statically links libdigidocpp (LGPL-2.1-or-later). Under LGPL Section 6,
you have the right to modify libdigidocpp and rebuild pydigidoc with your changes.

## Prerequisites

- Python 3.10+
- CMake 3.20+
- SWIG 4.0+
- C++23 compiler (GCC 13+, Clang 16+, MSVC 2022+)
- OpenSSL 3.0+, libxml2, zlib, xmlsec1

## Rebuilding from source distribution

```bash
# Extract the sdist (includes full libdigidocpp source)
tar xzf pydigidoc-*.tar.gz
cd pydigidoc-*

# Make your modifications to libdigidocpp/
# e.g., edit libdigidocpp/src/Container.cpp

# Rebuild
uv build --wheel
uv add dist/*.whl
```

## Rebuilding from git

```bash
git clone --recurse-submodules https://github.com/namespace-ee/pydigidoc.git
cd pydigidoc

# Make your modifications to the libdigidocpp/ submodule

# Rebuild
uv build --wheel
uv add dist/*.whl
```
