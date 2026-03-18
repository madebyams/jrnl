from conan import ConanFile
from conan.tools.files import get, copy
from conan.tools.build import check_min_cppstd
import os


class WebviewConan(ConanFile):
    name = "webview"
    version = "0.12.0"
    description = "Tiny cross-platform webview library for C/C++"
    license = "MIT"
    url = "https://github.com/webview/webview"
    homepage = "https://github.com/webview/webview"
    topics = ("webview", "gui", "html", "javascript", "webkit")
    package_type = "header-library"
    settings = "os", "compiler", "build_type", "arch"
    no_copy_source = True

    def validate(self):
        check_min_cppstd(self, 17)

    def source(self):
        get(
            self,
            "https://github.com/webview/webview/archive/refs/tags/0.12.0.tar.gz",
            strip_root=True,
        )

    def package(self):
        copy(
            self,
            "LICENSE",
            src=self.source_folder,
            dst=os.path.join(self.package_folder, "licenses"),
        )
        # webview 0.12 keeps public headers under core/include/
        copy(
            self,
            "*.h",
            src=os.path.join(self.source_folder, "core", "include"),
            dst=os.path.join(self.package_folder, "include"),
        )
        copy(
            self,
            "*.hh",
            src=os.path.join(self.source_folder, "core", "include"),
            dst=os.path.join(self.package_folder, "include"),
        )

    # Header-only: package id does not depend on compiler / build type
    def package_id(self):
        self.info.clear()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "webview")
        self.cpp_info.set_property("cmake_target_name", "webview::core")

        # Header-only — no lib or bin artifacts
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []

        if self.settings.os == "Macos":
            self.cpp_info.frameworks = ["WebKit", "Cocoa"]

        elif self.settings.os == "Windows":
            # Requires the WebView2 SDK; link against the shell/COM helpers
            self.cpp_info.system_libs = ["ole32", "shell32", "shlwapi", "version"]
            self.cpp_info.defines = ["WEBVIEW_EDGE"]

        elif self.settings.os == "Linux":
            # Requires system packages: libgtk-3-dev libwebkit2gtk-4.1-dev
            # (or libwebkit2gtk-4.0-dev on older distros)
            self.cpp_info.defines = ["WEBVIEW_GTK"]
            # Flags are resolved by pkg-config at build time (see CMakeLists.txt)
            self.cpp_info.set_property("cmake_find_mode", "none")
