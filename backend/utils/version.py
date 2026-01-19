"""
Version Utility - Get Application Version

Author: Shenzhen Wang & AI
License: MIT
"""
from pathlib import Path

__version__ = "1.0.0"


def get_version() -> str:
    """
    Get version from VERSION file or fallback to __version__
    
    Returns:
        Version string
    """
    try:
        version_file = Path(__file__).parent.parent.parent / 'VERSION'
        if version_file.exists():
            return version_file.read_text().strip()
    except Exception:
        pass
    return __version__
