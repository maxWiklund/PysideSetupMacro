import os
import sys
import subprocess

try:
    import PySide6 as pyside
except ImportError:
    try:
        import PySide2 as pyside
    except ImportError:
        raise ModuleNotFoundError("No PySide module found!")


QT_ROOT = os.path.dirname(pyside.__file__)


def get_app(qt_tool: str) -> str:
    if sys.platform != "win32":
        return os.path.join(QT_ROOT, "Qt", "libexec", qt_tool)
    return os.path.join(QT_ROOT, qt_tool)  # TODO: Confirm if this is the case for windows.


def compile_qresource(source: str, destination: str) -> None:
    args = [get_app("rcc"), source, "-g", "python", "-o", destination]
    subprocess.run(" ".join(args), shell=True)


def convert_ui_file(source: str, destination: str) -> None:
    args = [get_app("uic"), source, "-g", "python", "-o", destination]
    subprocess.run(" ".join(args), shell=True)
