# DekTec DTAPI Conan package

This repository contains a conan package recipe allowing to easily link with DekTec DTAPI.

# Downloads
  The complete installers which has been used to build this package can be downloaded at the following urls :

* For Windows : https://files.trilogic.fr/public/7927e8/dl/WinSDK_v2020.01.0.zip

# Usage

## Basic setup
$ conan install dektec-dtapi/xxxx.x@trilogic/stable

## Project setup

### From a conanfile.py
```python
def build_requirements (self)
    self.requires("dektec-dtapi/xxxx.x@trilogic/stable")
```

### From a conanfile.txt
```python
[build_requires]
dektec-dtapi/xxxx.x@trilogic/stable
```