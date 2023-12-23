from setuptools import find_packages, setup

from pyside_setup_macro import QtBuildPackage
import skandinavia_flag_picker


setup(
    name="skandinavia_flag_picker",
    version=skandinavia_flag_picker.__version__,
    packages=find_packages(exclude=("test*", "tests*")),
    url="",
    license="Apache License, Version 2.0",
    author="Max Wiklund",
    author_email="",
    description="Demo project",
    cmdclass={
        "build_py": QtBuildPackage,
    },
)
