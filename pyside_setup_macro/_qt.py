# Copyright (C) 2023  Max Wiklund
#
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
    """Get path to qt app.

    Args:
        qt_tool: Name of qt app.

    Returns:
        Path to qt app.

    """
    if sys.platform != "win32":
        return os.path.join(QT_ROOT, "Qt", "libexec", qt_tool)
    return os.path.join(QT_ROOT, qt_tool)


def compile_qresource(source: str, destination: str) -> None:
    """Compile qresource file rcc.

    Args:
        source: File path to qresource file.
        destination: Output file path.

    """
    args = [get_app("rcc"), source, "-g", "python", "-o", destination]
    subprocess.run(" ".join(args), shell=True)


def compile_ui_file(source: str, destination: str) -> None:
    """Compile .ui file to python module with uic.

    Args:
        source: File path to .ui file.
        destination: Output file path.

    """
    args = [get_app("uic"), source, "-g", "python", "-o", destination]
    subprocess.run(" ".join(args), shell=True)
