# DekTec DTAPI Conan package

This repository contains a conan package recipe allowing to easily link with DekTec DTAPI.

# Downloads
  The complete installers which has been used to build this package can be downloaded at the following urls :

* For Linux   : https://files.trilogic.fr/public/dektec-linux/dl/LinuxSDK_v2018.07.0.tar.gz
* For Windows : https://files.trilogic.fr/public/dektec-windows/dl/WinSDK_v2018.07.0.zip

# Usage

## Basic setup
$ conan install dektec-dtapi/1807.0@trilogic/stable

## Project setup

### From a conanfile.py
```python
def build_requirements (self)
    self.requires("dektec-dtapi/1807.0@trilogic/stable")
```

### From a conanfile.txt
```python
[build_requires]
dektec-dtapi/1807.0@trilogic/stable
```