from conans import ConanFile, tools
from conans.errors import ConanException
import os

#
# Winsdk 64-bits.
#
def download_x86_64_winsdk (self):
    if 'Release' in self.settings.build_type:
        if 'MD' in self.settings.compiler.runtime:
            tools.get ('https://files.trilogic.fr/public/cbfbe1/dl/vc16_x86_64_md_release.zip')
        else:
            tools.get ('https://files.trilogic.fr/public/204474/dl/vc16_x86_64_mt_release.zip')
    else:
        if 'MD' in self.settings.compiler.runtime:
            tools.get ('https://files.trilogic.fr/public/2988e9/dl/vc16_x86_64_md_debug.zip')
        else:
            tools.get ('https://files.trilogic.fr/public/4980ce/dl/vc16_x86_64_mt_debug.zip')

#
# Winsdk 32-bits.
#
def download_x86_winsdk (self):
    if 'Release' in self.settings.build_type:
        if 'MD' in self.settings.compiler.runtime:
            tools.get ('https://files.trilogic.fr/public/62a8ab/dl/vc16_x86_md_release.zip')
        else:
            tools.get ('https://files.trilogic.fr/public/672c83/dl/vc16_x86_mt_release.zip')
    else:
        if 'MD' in self.settings.compiler.runtime:
            tools.get ('https://files.trilogic.fr/public/47dc0c/dl/vc16_x86_md_debug.zip')
        else:
            tools.get ('https://files.trilogic.fr/public/142d69/dl/vc16_x86_mt_debug.zip')

#
# Dektec Conan package.
#
class DektecDtapiConan (ConanFile):
    name = "dektec-dtapi"
    version = "2003.0"
    settings = "os", "arch_build", "compiler", "build_type"
    description = "Dektec DTAPI"
    url = "http://www.dektec.com"
    author = "Dektec Digital Video B.V."
    license = "Dektec"
    exports = "DtSdiFileFmt.h", "LICENSE"
    description = "C++ API for development of custom applications with DekTec devices."

    def source (self):
        if self.settings.os == "Linux":
            package = 'LinuxSDK_v2020.03.0.tar.gz'
            tools.get ('https://files.trilogic.fr/public/032355/dl/' + package)

    def build (self):
        if self.settings.os == "Linux":
            if self.settings.arch_build == 'x86_64':
                self.run ('ar cru libdtapi.a LinuxSDK/DTAPI/Lib/GCC5.1_CXX11_ABI1/DTAPI64.o')
            if self.settings.arch_build =='x86':
                self.run ('ar cru libdtapi.a LinuxSDK/DTAPI/Lib/GCC5.1_CXX11_ABI1/DTAPI.o')
        elif self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            # Do some check againt static runtime to inform user.
            if self.settings.compiler.version != 16:
                if 'MT' in self.settings.compiler.runtime:
                    raise ConanException('Visual Studio 19 (VC16) is required, yours is VC%s' % self.settings.compiler.version)
                else:
                    self.output.warn ('Visual Studio 19 (VC16) redist will be needed !')
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
