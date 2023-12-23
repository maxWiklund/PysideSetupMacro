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

import pyside_setup_macro

setup(
    name="pyside_setup_macro",
    version=pyside_setup_macro.__version__,
    packages=find_packages(exclude=("test*", "tests*", "exampels*")),
    url="https://github.com/maxWiklund/PysideSetupMacro",
    license="Apache License, Version 2.0",
    author="Max Wiklund",
    author_email="",
    description="Build tools to compile and generate QT qresource files and .ui files at build time (Pyside).",
)
