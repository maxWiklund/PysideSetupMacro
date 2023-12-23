![PySide Setup Macro](logo.png)

## Introduction
Build tools to compile and generate QT qresource files and .ui files at build time (Pyside).

Are you tired of maintaining a qresource files and converting .ui? Then your at the right place.
PysideSetupMacro converts all qresource files and .ui files for you at build time. 
All you have to do is to import the module in your `setup.py` and use it.

**example**
```python

from setuptools import find_packages, setup

from pyside_setup_macro import QtBuildPackage

setup(
    ...,
    packages=find_packages(exclude=("test*", "tests*")),
    ...,
    cmdclass={
        "build_py": QtBuildPackage,  # This is all you need to add.
    },
)
```


If your lazy like me and don't want to maintain a qresource file then I have introduced qmacro.

The qmacro has 2 parts. 
A mandatory name of the qresource file to ge created.
```python
name="resource"  # Name of resource file to be created.
```

A built-in function call for creating the resources.
```python
add_files("*.png", prefix="/images")  # Individually specify the prefixes.
```


With the following dir structure you can create the resource file in 2 ways.
```
├── __init__.py
├── flags
│   ├── denmark.png
│   ├── norway.png
│   └── sweden.png
├── pen.png
└── qmacro
```
### Option 1
`qmacro`
```python
name = "qresource"
add_files("flags/*.png", prefix="flags")
add_files("*.png")
```

**Resulting qresource file**
```xml
<?xml version="1.0" ?>
<RCC>
   <qresource prefix="">
      <file alias="pen.png">pen.png</file>
   </qresource>
   <qresource prefix="flags">
      <file alias="denmark.png">flags/denmark.png</file>
      <file alias="norway.png">flags/norway.png</file>
      <file alias="sweden.png">flags/sweden.png</file>
   </qresource>
</RCC>
```

### Option 2

`qmacro`
```python
name = "qresource"
walk()
```

**Resulting qresource file**
```xml
<?xml version="1.0" ?>
<RCC>
   <qresource prefix="">
      <file alias="pen.png">pen.png</file>
   </qresource>
   <qresource prefix="flags">
      <file alias="denmark.png">flags/denmark.png</file>
      <file alias="norway.png">flags/norway.png</file>
      <file alias="sweden.png">flags/sweden.png</file>
   </qresource>
</RCC>
```