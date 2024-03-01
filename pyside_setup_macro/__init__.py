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
import shutil
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop
from pyside_setup_macro import _qmacro, _qt

__version__ = "0.1.1"


def _create_build_dir(path: str) -> None:
    """Create build directory path.

    Args:
        path: Directory path to create.

    """
    if not os.path.exists(path):
        os.makedirs(path)


def _file_needs_processing(file_name: str) -> bool:
    return file_name == "qmacro" or file_name.endswith((".qrc", ".ui"))


def _convert_qrc(source_path: str, destination_dir: str, file: str) -> None:
    """Compile qresource file.

    Args:
        source_path: Source qresource file to compile.
        destination_dir: Build directory to put compiled python module in.
        file: File name of qresource.

    """
    resource_name = file.replace(".qrc", ".py")
    _qt.compile_qresource(source_path, os.path.join(destination_dir, resource_name))


def _convert_ui_files(source_path: str, destination_dir: str, file: str) -> None:
    """Compile .ui file.

    Args:
        source_path: Source ui. file to compile.
        destination_dir: Build directory to put compiled python module in.
        file: File name of .ui file.

    """
    resource_name = file.replace(".ui", ".py")
    _qt.compile_ui_file(source_path, os.path.join(destination_dir, resource_name))


def _compile_file(source_path, destination_dir, file) -> None:
    if source_path.endswith(".qrc"):
        # A Qt Resource file has been found. it needs to be compiled and moved to build dir.
        _convert_qrc(source_path, destination_dir, file)
    elif source_path.endswith(".ui"):
        _convert_ui_files(source_path, destination_dir, file)
    elif file == "qmacro":
        _qmacro.create_and_compile_qresource(source_path, destination_dir)


def compile_qt_files(root_dir) -> None:
    """Compile qt files in director

    Args:
        root_dir: Root dir to find file in.


    """
    # Travers source code and compile any qt file in package.
    for root, _, files in os.walk(root_dir):
        for file in files:
            if _file_needs_processing(file):
                _compile_file(os.path.join(root, file), root, file)


class QtBuildPackage(build_py):
    """Build class that can compile qt files."""

    def _compile_and_move_qt_files(self) -> None:
        """Compile qt files and move them to build dir."""
        if os.path.exists(self.build_lib):
            shutil.rmtree(self.build_lib)

        root_packages = {
            path.split(os.path.sep).pop(0) for path in self.get_source_files()
        }

        package_root = self.package_dir.get("", ".")
        # Travers source code and compile any qt file.
        for package in root_packages:
            for root, _, files in os.walk(package):
                for file in files:
                    destination_dir = os.path.join(
                        self.build_lib, os.path.relpath(root, package_root)
                    )
                    source_path = os.path.join(root, file)
                    if _file_needs_processing(file):
                        _create_build_dir(destination_dir)
                        _compile_file(source_path, destination_dir, file)

    def run(self) -> None:
        """Convert qt files and build python package."""
        self._compile_and_move_qt_files()
        super().run()  # Run normal installation.


class QtBuildDevelop(develop):
    """Build class that can compile qt files in dev-mode."""

    def run(self) -> None:
        """Convert qt files locally and configure package in dev-mode."""
        compile_qt_files(self.dist.module_path)
        super().run()
