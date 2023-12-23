import os
import shutil
from setuptools.command.build_py import build_py
from pyside_setup_macro import _qmacro, _qt

__version__ = "0.1.0"


def _create_build_dir(path: str) -> None:
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


class QtBuildPackage(build_py):
    def compile_resource_files(self):
        package_root = "."
        for package in self.packages:
            for root, _, files in os.walk(package):
                for file in files:
                    destination_dir = os.path.join(self.build_lib, os.path.relpath(root, package_root))
                    source_path = os.path.join(root, file)
                    if source_path.endswith(".qrc"):
                        # A Qt Resource file has been found. it needs to be compiled and moved to build dir.
                        self.convert_qrc(source_path, destination_dir, file)
                    elif source_path.endswith(".ui"):
                        self._convert_ui_files(source_path, destination_dir, file)
                    elif file == "qmacro":
                        _create_build_dir(destination_dir)
                        _qmacro.create_and_compile_qresource(source_path, destination_dir)

    def convert_qrc(self, source_path: str, destination_dir: str, file: str):
        _create_build_dir(destination_dir)
        resource_name = file.replace(".qrc", ".py")
        _qt.compile_qresource(source_path, os.path.join(destination_dir, resource_name))

    def _convert_ui_files(self, source_path: str, destination_dir: str, file: str) -> None:
        _create_build_dir(destination_dir)
        resource_name = file.replace(".ui", ".py")
        _qt.convert_ui_file(source_path, os.path.join(destination_dir, resource_name))

    def run(self) -> None:
        self.compile_resource_files()
        super().run()
