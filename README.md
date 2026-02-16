# pydigidoc

Python bindings for [libdigidocpp](https://github.com/open-eid/libdigidocpp) — create, validate and handle digitally signed documents (ASiC-E, BDOC, etc).

## Installation

```bash
pip install pydigidoc
```

## Usage

```python
import pydigidoc

# Initialize the library
pydigidoc.initialize("MyApp")

# Create a container and add files
doc = pydigidoc.Container.create("document.asice")
doc.add_data_file("report.pdf", "application/pdf")

# Sign with a PKCS#12 certificate
signer = pydigidoc.PKCS12Signer("certificate.p12", "password")
doc.sign(signer)
doc.save()

# Open and verify an existing container
doc = pydigidoc.Container.open("document.asice")
for sig in doc.signatures():
    print(f"Signed by: {sig.signed_by()}")
    sig.validate()

# Clean up
pydigidoc.terminate()
```

## Building from source

### Prerequisites

- Python 3.10+
- CMake 3.20+
- SWIG 4.0+
- C++23 compiler (GCC 13+, Clang 16+, MSVC 2022+)
- OpenSSL 3.0+, libxml2, zlib, xmlsec1

### Build

```bash
git clone --recurse-submodules https://github.com/namespace-ee/pydigidoc.git
cd pydigidoc
pip install .
```

## License

LGPL-2.1-or-later. See [LICENSE](LICENSE) for the full text and [RELINKING.md](RELINKING.md) for relinking instructions.
