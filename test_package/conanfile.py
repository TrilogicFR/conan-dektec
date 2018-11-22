import os

from conans import ConanFile, CMake, tools

class DtApiTestConan (ConanFile):
  settings = "os", "compiler", "build_type", "arch"
  generators = "cmake"

  def build (self):
    cmake = CMake (self)
    # Current dir is "test_package/build/<build_id>"
    # and CMakeLists.txt is in "test_package".
    cmake.configure ()
    cmake.build ()

  def test(self):
    # equal to ./bin/scandev, but portable win: .\bin\scandev
    if not tools.cross_building(self.settings):
      self.run(os.sep.join([".","bin", "scandev"]))
