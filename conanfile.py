from conans import ConanFile, tools
import os

#
# Visual Studio helpers.
#
def download_winsdk_vc15 (arch, runtime):
    if arch == 'x86_64':
        if runtime == 'MD':
            tools.download ('https://files.trilogic.fr/public/vc15-x86-64-md/dl/winsdk_vc15_x86_64_md.zip', 'winsdk.zip')
        else:
            tools.download ('https://files.trilogic.fr/public/vc15-x86-64-mt/dl/winsdk_vc15_x86_64_mt.zip', 'winsdk.zip')
    else:
        if runtime == 'MD':
            tools.download ('https://files.trilogic.fr/public/vc15-x86-md/dl/winsdk_vc15_x86_md.zip', 'winsdk.zip')
        else:
            tools.download ('https://files.trilogic.fr/public/vc15-x86-mt/dl/winsdk_vc15_x86_mt.zip', 'winsdk.zip')

#
# Visual Studio multi-config.
#
def download_winsdk (settings):
    if settings.compiler.version == 15:
        download_winsdk_vc15 (settings.arch_build, settings.compiler.runtime)
    else:
      raise ConanException ("Visual Studio " + settings.compiler.version + " is not supported")

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
            download_winsdk (self.settings)
            tools.unzip ('winsdk.zip')
        else:
          raise ConanException (self.settings.os + "/" + self.settings.compiler + " is not supported")

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
        self.cpp_info.libs = tools.collect_libs (self)
        if self.settings.os == "Windows":
          self.cpp_info.debug.libs = ["%s_d" % (self.name)]
          self.cpp_info.release.libs = ["%s" % (self.name)]
        else:
          self.cpp_info.libs.append ('pthread')
          self.cpp_info.libs.append ('dl')
