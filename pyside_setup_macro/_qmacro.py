from typing import List, Tuple
import glob

from xml.dom import minidom
import xml.etree.ElementTree as ET
import os

from pyside_setup_macro._qt import compile_qresource


_SUPPORTED_FILE_EXT = (".exr", ".png", ".jpeg", ".tiff", ".svg", ".gif")


def create_resources(root: ET.Element, file_names: List[str], prefix: str) -> None:
    node = ET.Element("qresource", {"prefix": prefix})
    root.append(node)

    for file in file_names:
        element = ET.Element("file")
        element.attrib["alias"] = os.path.basename(file)
        element.text = file
        node.append(element)


class QtMacroError(Exception):
    ...


class QrcTarget:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.patterns = []

    def add_files(self, pattern: str, prefix="") -> None:
        files = glob.glob(os.path.join(self.root_dir, pattern))
        files = [os.path.relpath(file, self.root_dir) for file in files]
        self.patterns.append((files, prefix))

    def walk(self) -> None:
        for root, _, files in os.walk(self.root_dir):
            prefix = os.path.relpath(root, self.root_dir).replace(".", "")
            paths = [os.path.normpath(os.path.join(root, file)) for file in files if file.endswith(_SUPPORTED_FILE_EXT)]
            paths = list(filter(os.path.isfile, paths))
            paths = list(os.path.relpath(path, self.root_dir) for path in paths)
            paths.sort()
            if paths:
                self.patterns.append((paths, prefix))


def create_and_compile_qresource(source_file: str, build_dir: str) -> None:
    target_cls = QrcTarget(os.path.dirname(source_file))
    _target_data = {
        "__file__": source_file,
        "__name__": "__main__",
        "add_files": target_cls.add_files,
        "walk": target_cls.walk,
    }
    with open(source_file) as f:
        exec(f.read(), _target_data)
        name = _target_data.get("name")
        if not name:
            raise QtMacroError("name is missing. Add a name like this 'name=\"resource\"'")

    root_et = ET.Element("RCC")
    for files, prefix in target_cls.patterns:
        create_resources(root_et, files, prefix)

    resource_file = os.path.join(os.path.dirname(source_file), f"{_target_data['name']}.qrc")
    xmlstr = minidom.parseString(ET.tostring(root_et)).toprettyxml(indent="   ")
    with open(resource_file, "w") as f:
        f.write(xmlstr)

    compile_qresource(resource_file, os.path.join(build_dir, f"{_target_data['name']}.py"))
    os.remove(resource_file)  # Remove resou
