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

from setuptools import find_packages, setup

from pyside_setup_macro import QtBuildPackage, QtBuildDevelop
import scandinavian_flag_picker


setup(
    name="scandinavian_flag_picker",
    version=scandinavian_flag_picker.__version__,
    packages=find_packages(exclude=("test*", "tests*")),
    url="",
    license="Apache License, Version 2.0",
    author="Max Wiklund",
    author_email="",
    description="Demo project",
    cmdclass={"build_py": QtBuildPackage, "develop": QtBuildDevelop},
    install_requires=["PySide6"],
)
