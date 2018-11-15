from conans import ConanFile, tools
import os

def get_version():
    if 'CI_COMMIT_REF_NAME' in os.environ:
        return os.environ.get ('CI_COMMIT_REF_NAME')
    git = tools.Git ()
    try:
        return "%s" % (git.get_branch ())
    except:
        return None

class DektecDtapiConan(ConanFile):
    name = "dektec-dtapi"
    version = get_version ()
    settings = "os", "arch"
    description = "Dektec DTAPI"
    url = "None"
    license = "None"

    def source(self):
        if self.settings.os == "Linux":
            tools.download('http://192.168.42.210/dektec/LinuxSDK/LinuxSDK_2018_July_2018.zip', 'LinuxSDK_2018_July_2018.tar.gz')
            tools.unzip ('LinuxSDK_2018_July_2018.tar.gz')
            self.run ('ar cru dtapi.a LinuxSDK/DTAPI/Lib/GCC4.4/DTAPI64.o')

    def package(self):
        if self.settings.os == "Windows":
            self.copy ("*")
        else:
            self.copy("*", dst="include", src="LinuxSDK/DTAPI/Include")
            self.copy("dtapi.a", dst="lib")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
