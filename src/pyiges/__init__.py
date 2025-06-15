"""pyiges module."""

from importlib.metadata import PackageNotFoundError, version

from pyiges.iges import Iges, read

try:
    __version__ = version("pyminiply")
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["read", "Iges", "__version__"]
