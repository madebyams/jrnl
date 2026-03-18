from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMakeDeps


class JrnlConan(ConanFile):
    name = "jrnl"
    version = "0.1.0"
    settings = "os", "compiler", "build_type", "arch"

    def requirements(self):
        self.requires("webview/0.12.0")

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()
