"""pyiges module."""

from importlib.metadata import PackageNotFoundError, version

from pyiges.iges import Iges, read
from pyiges.reader import read_as_mesh

try:
    __version__ = version("pyiges")
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["Iges", "__version__", "read", "read_as_mesh"]
