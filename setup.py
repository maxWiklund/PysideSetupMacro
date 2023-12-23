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
