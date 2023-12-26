from setuptools import find_packages, setup

from pyside_setup_macro import QtBuildPackage, QtBuildDevelop
import email_app


setup(
    name="email_app",
    version=email_app.__version__,
    packages=find_packages(exclude=("test*", "tests*")),
    url="",
    license="Apache License, Version 2.0",
    author="Max Wiklund",
    author_email="",
    description="Demo project",
    cmdclass={"build_py": QtBuildPackage, "develop": QtBuildDevelop},
    install_requires=["PySide6"],
)
