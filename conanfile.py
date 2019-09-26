from conans import ConanFile, tools
from conans.errors import ConanException
import os

#
# /MD configuration.
#
def download_winsdk_md (self):
    # For now, ONLY VC15 package is avail.
    if self.settings.compiler.version != 15:
        self.output.warn ('Visual Studio 15 redist will be needed !')

    if self.settings.arch_build == 'x86_64':
        tools.download ('https://files.trilogic.fr/public/vc15-x86-64-md/dl/winsdk_vc15_x86_64_md.zip', 'winsdk.zip')
    else:
        tools.download ('https://files.trilogic.fr/public/vc15-x86-md/dl/winsdk_vc15_x86_md.zip', 'winsdk.zip')

def download_winsdk_mt (self):
    # For now, ONLY VC15 package is avail.
    if self.settings.compiler.version != 15:
        raise ConanException('VC15 is required, yours is VC%s' % self.settings.compiler.version)

    if self.settings.arch_build == 'x86_64':
        tools.download ('https://files.trilogic.fr/public/vc15-x86-64-mt/dl/winsdk_vc15_x86_64_mt.zip', 'winsdk.zip')
    else:
        tools.download ('https://files.trilogic.fr/public/vc15-x86-mt/dl/winsdk_vc15_x86_mt.zip', 'winsdk.zip')

#
# Dektec Conan package.
#
class DektecDtapiConan (ConanFile):
    name = "dektec-dtapi"
    version = "1807.0"
    settings = "os", "arch_build", "compiler"
    description = "Dektec DTAPI"
    url = "http://www.dektec.com"
    author = "Dektec Digital Video B.V."
    license = "Dektec"
    exports = "DtSdiFileFmt.h", "LICENSE"
    description = "C++ API for development of custom applications with DekTec devices."

    def source (self):
        if self.settings.os == "Linux":
            package = 'LinuxSDK_v2018.07.0.tar.gz'
            tools.download ('https://files.trilogic.fr/public/dektec-linux/dl/' + package, package)
            tools.unzip (package)

    def build (self):
        if self.settings.os == "Linux":
            if self.settings.arch_build == 'x86_64':
                self.run ('ar cru libdtapi.a LinuxSDK/DTAPI/Lib/GCC4.4/DTAPI64.o')
            if self.settings.arch_build =='x86':
                self.run ('ar cru libdtapi.a LinuxSDK/DTAPI/Lib/GCC4.4/DTAPI.o')
        elif self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            if "MD" in self.settings.compiler.runtime:
                download_winsdk_md (self)
            else:
                download_winsdk_mt (self)
            tools.unzip ('winsdk.zip')
        else:
          raise ConanException ("Unsupported os/arch_build/compiler !")

    def package (self):
        if self.settings.os == "Windows":
            self.copy ("*.h", dst="include")
            self.copy ("*.lib", dst="lib")
        else:
            self.copy ("*", dst="include", src="LinuxSDK/DTAPI/Include")
            self.copy ("DtSdiFileFmt.h", dst="include")
            self.copy ("libdtapi.a", dst="lib")
            self.copy ("LICENSE", dst="")

    def package_info (self):
        if self.settings.os == "Windows":
            if self.settings.arch_build == 'x86_64':
                if "MD" in self.settings.compiler.runtime:
                    self.cpp_info.debug.libs = ["DTAPI64MDd"]
                    self.cpp_info.release.libs = ["DTAPI64MD"]
                else:
                    self.cpp_info.debug.libs = ["DTAPI64MTd"]
                    self.cpp_info.release.libs = ["DTAPI64MT"]
            else:
                if "MD" in self.settings.compiler.runtime:
                    self.cpp_info.debug.libs = ["DTAPIMDd"]
                    self.cpp_info.release.libs = ["DTAPIMD"]
                else:
                    self.cpp_info.debug.libs = ["DTAPIMTd"]
                    self.cpp_info.release.libs = ["DTAPIMT"]
        else:
            self.cpp_info.libs = tools.collect_libs (self)
            self.cpp_info.libs.append ('pthread')
            self.cpp_info.libs.append ('dl')
