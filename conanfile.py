from conans import ConanFile, tools
from conans.errors import ConanException
import os

#
# Winsdk 64-bits.
#
def download_x86_64_winsdk (self):
    if 'Release' in self.settings.build_type:
        if 'MD' in self.settings.compiler.runtime:
            tools.get ('https://files.trilogic.fr/public/483618/dl/vc17_x86_64_md_release.zip')
        else:
            tools.get ('https://files.trilogic.fr/public/b6adf7/dl/vc17_x86_64_mt_release.zip')
    else:
        if 'MD' in self.settings.compiler.runtime:
            tools.get ('https://files.trilogic.fr/public/bc00b0/dl/vc17_x86_64_md_debug.zip')
        else:
            tools.get ('https://files.trilogic.fr/public/f1d800/dl/vc17_x86_64_mt_debug.zip')

#
# Winsdk 32-bits.
#
def download_x86_winsdk (self):
    if 'Release' in self.settings.build_type:
        if 'MD' in self.settings.compiler.runtime:
            tools.get ('https://files.trilogic.fr/public/7b81c0/dl/vc17_x86_md_release.zip')
        else:
            tools.get ('https://files.trilogic.fr/public/318f40/dl/vc17_x86_mt_release.zip')
    else:
        if 'MD' in self.settings.compiler.runtime:
            tools.get ('https://files.trilogic.fr/public/ab7798/dl/vc17_x86_md_debug.zip')
        else:
            tools.get ('https://files.trilogic.fr/public/06a3bd/dl/vc17_x86_mt_debug.zip')

#
# Dektec Conan package.
#
class DektecDtapiConan (ConanFile):
    name = "dektec-dtapi"
    version = "1907.1"
    settings = "os", "arch_build", "compiler", "build_type"
    description = "Dektec DTAPI"
    url = "http://www.dektec.com"
    author = "Dektec Digital Video B.V."
    license = "Dektec"
    exports = "DtSdiFileFmt.h", "LICENSE"
    description = "C++ API for development of custom applications with DekTec devices."

    def source (self):
        if self.settings.os == "Linux":
            package = 'LinuxSDK_v2019.07.1.tar.gz'
            tools.get ('https://files.trilogic.fr/public/6bac4f/dl/' + package)

    def build (self):
        if self.settings.os == "Linux":
            if self.settings.arch_build == 'x86_64':
                self.run ('ar cru libdtapi.a LinuxSDK/DTAPI/Lib/GCC5.1_CXX11_ABI1/DTAPI64.o')
            if self.settings.arch_build =='x86':
                self.run ('ar cru libdtapi.a LinuxSDK/DTAPI/Lib/GCC5.1_CXX11_ABI1/DTAPI.o')
        elif self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            # Do some check againt static runtime to inform user.
            if self.settings.compiler.version != 15:
                if 'MT' in self.settings.compiler.runtime:
                    raise ConanException('Visual Studio 17 (VC15) is required, yours is VC%s' % self.settings.compiler.version)
                else:
                    self.output.warn ('Visual Studio 17 (VC15) redist will be needed !')
            # Download requested Winsdk.
            if self.settings.arch_build == 'x86_64':
                download_x86_64_winsdk (self)
            else:
                download_x86_winsdk (self)
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
            self.cpp_info.defines = [ "_GLIBCXX_USE_CXX11_ABI=1" ]
            self.cpp_info.libs = tools.collect_libs (self)
            self.cpp_info.libs.append ('pthread')
            self.cpp_info.libs.append ('dl')
