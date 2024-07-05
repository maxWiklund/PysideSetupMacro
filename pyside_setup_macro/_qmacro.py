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

from typing import List
from xml.dom import minidom
import glob
import os
import re
import xml.etree.ElementTree as ET

from pyside_setup_macro._qt import compile_qresource


_SUPPORTED_FILE_EXT = (".exr", ".png", ".jpeg", ".tiff", ".svg", ".gif", ".ttf")
_FILE_NAME_RE = re.compile(r"^[a-zA-Z_][\w_]+$")


def _create_resources(root: ET.Element, file_names: List[str], prefix: str) -> None:
    """Create file resources for prefix.

    Args:
        root: Root xml node.
        file_names: List of file names.
        prefix (optional): Prefix to use.

    """
    node = ET.Element("qresource", {"prefix": prefix})
    root.append(node)

    for file in file_names:
        element = ET.Element("file", {"alias": os.path.basename(file)})
        element.text = file
        node.append(element)


class QMacroError(Exception):
    """Exception for qmacro."""

    ...


class QrcTarget:
    """Code to execute qmacro."""

    def __init__(self, root_dir: str):
        """Initialize class and do nothing.

        Args:
            root_dir: Root directory of qmacro file.

        """
        self.root_dir = root_dir
        self.patterns = []

    def add_files(self, pattern: str, prefix: str = "") -> None:
        """Add files macro. executed in the qmacro file.

        Args:
            pattern: Pattern to use when finding resources.
            prefix (optional): Prefix to add.

        """
        files = glob.glob(os.path.join(self.root_dir, pattern))
        files = [os.path.relpath(file, self.root_dir) for file in files]
        self.patterns.append((files, prefix))

    def walk(self) -> None:
        """Qmacro function to walk direcories and add resources."""
        for root, _, files in os.walk(self.root_dir):
            prefix = os.path.relpath(root, self.root_dir).replace(".", "")
            paths = [
                os.path.normpath(os.path.join(root, file))
                for file in files
                if file.endswith(_SUPPORTED_FILE_EXT)
            ]
            paths = list(filter(os.path.isfile, paths))
            paths = list(os.path.relpath(path, self.root_dir) for path in paths)
            paths.sort()
            if paths:
                self.patterns.append((paths, prefix))


def create_and_compile_qresource(source_file: str, build_dir: str) -> None:
    """Create qresource file from qmacro and compile it.

    Args:
        source_file: File path to qmacro file.
        build_dir: Build directory to move created qresource to.

    """
    target_cls = QrcTarget(os.path.dirname(source_file))
    _target_data = {
        "__file__": source_file,
        "__name__": "__main__",
        "add_files": target_cls.add_files,
        "walk": target_cls.walk,
    }
    with open(source_file, encoding="utf8") as f:
        exec(f.read(), _target_data)
        name = _target_data.get("name")
        if not name:
            raise QMacroError(
                "name is missing. Add a name like this 'name=\"resource\"'"
            )
        if " " in name:
            raise QMacroError(
                f'You are not allowed to have spaces in name "{name}" {source_file}'
            )
        if not _FILE_NAME_RE.match(name):
            raise QMacroError(f'"{name}" is invalid. [a-zA-Z_][\w_]+')

    root_et = ET.Element("RCC")
    for files, prefix in target_cls.patterns:
        _create_resources(root_et, files, prefix)

    resource_file = os.path.join(
        os.path.dirname(source_file), f"{_target_data['name']}.qrc"
    )
    xmlstr = minidom.parseString(ET.tostring(root_et)).toprettyxml(indent="   ")
    with open(resource_file, "w") as f:
        f.write(xmlstr)

    compile_qresource(
        resource_file, os.path.join(build_dir, f"{_target_data['name']}.py")
    )
    os.remove(resource_file)  # Remove qresource file.
