from CoT import xml
from CoT.models import Event, Point

__extensions_installed__ = {"milstd": True, "mitre": True}

try:
    import pycot_ext_mitre as mitre
except ImportError:

    # Handle the case where MITRE-specific dependencies aren't installed
    __extensions_installed__["mitre"] = False


try:
    import pycot_ext_milstd as milstd
except ImportError:
    # Handle the case where MILSTD-specific dependencies aren't installed
    __extensions_installed__["milstd"] = False
