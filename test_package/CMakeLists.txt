cmake_minimum_required (VERSION 2.8.12)
project (PackageTest CXX)

include (${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup ()

add_executable (scandev main.cpp)
target_link_libraries (scandev ${CONAN_LIBS})