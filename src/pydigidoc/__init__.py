"""
pydigidoc - Python bindings for libdigidocpp

Create, validate and handle digitally signed documents (ASiC-E, BDOC, etc).
"""

from __future__ import annotations

import os as _os

from pydigidoc.digidoc import (
    # Module-level functions (already snake_case or lowercase)
    terminate,
    version,
    app_info,
    user_agent,
    initialize_lib as _initialize_lib_raw,
    # Container
    Container,
    ContainerOpenCB,
    # Data types
    DataFile,
    Signature,
    # Signers
    Signer,
    PKCS11Signer,
    PKCS12Signer,
    ExternalSigner,
    # Configuration
    Conf,
    ConfV2,
    ConfV3,
    ConfV4,
    ConfV5,
    XmlConf,
    DigiDocConf,
    # Container types (template instantiations)
    StringVector,
    StringMap,
    DataFiles,
    Signatures,
    TSAInfos,
    # Structs
    TSAInfo,
)

__version__ = "0.0.4"

# Path to bundled schema/config files
_SCHEMA_DIR = _os.path.join(_os.path.dirname(__file__), "schema")


def initialize(app_name: str = "libdigidocpp", user_agent: str = "") -> None:
    """Initialize the libdigidocpp library with bundled schema files.

    Uses the schema files bundled in the wheel so no system-wide
    installation of libdigidocpp is required.
    """
    if user_agent:
        _initialize_lib_raw(app_name, user_agent, _SCHEMA_DIR)
    else:
        _initialize_lib_raw(app_name, _SCHEMA_DIR)


def initialize_lib(app_name: str, path: str, user_agent: str = "") -> None:
    """Initialize with a custom schema/config directory."""
    if user_agent:
        _initialize_lib_raw(app_name, user_agent, path)
    else:
        _initialize_lib_raw(app_name, path)


__all__ = [
    "__version__",
    # Functions
    "initialize",
    "terminate",
    "version",
    "app_info",
    "user_agent",
    "initialize_lib",
    # Container
    "Container",
    "ContainerOpenCB",
    # Data types
    "DataFile",
    "Signature",
    # Signers
    "Signer",
    "PKCS11Signer",
    "PKCS12Signer",
    "ExternalSigner",
    # Configuration
    "Conf",
    "ConfV2",
    "ConfV3",
    "ConfV4",
    "ConfV5",
    "XmlConf",
    "DigiDocConf",
    # Container types
    "StringVector",
    "StringMap",
    "DataFiles",
    "Signatures",
    "TSAInfos",
    # Structs
    "TSAInfo",
]
