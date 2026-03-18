cmake_minimum_required(VERSION 3.22)

# ---------------------------------------------------------------------------
# Conan bootstrap — always runs so new dependencies in conanfile.py are picked
# up automatically on the next CMake configure.
# ---------------------------------------------------------------------------
find_program(CONAN conan REQUIRED DOC "Conan package manager")

set(_recipe_dir "${CMAKE_CURRENT_SOURCE_DIR}/recipes/webview")
set(_toolchain  "${CMAKE_CURRENT_BINARY_DIR}/conan_toolchain.cmake")

message(STATUS "[conan] Exporting local webview recipe...")
execute_process(
    COMMAND ${CONAN} export "${_recipe_dir}" --version 0.12.0
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMAND_ERROR_IS_FATAL ANY
)

message(STATUS "[conan] Running conan install...")
execute_process(
    COMMAND ${CONAN} install "${CMAKE_CURRENT_SOURCE_DIR}"
        --output-folder=${CMAKE_CURRENT_BINARY_DIR}
        --build=missing
        -s build_type=${CMAKE_BUILD_TYPE}
        -s compiler.cppstd=17
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMAND_ERROR_IS_FATAL ANY
)

if(NOT EXISTS "${_toolchain}")
    message(FATAL_ERROR
        "[conan] Toolchain not found after conan install — re-run CMake.")
endif()

include("${_toolchain}")

# ---------------------------------------------------------------------------
# Project
# ---------------------------------------------------------------------------
project(jrnl VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(webview REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter)

# On Linux webview depends on GTK3 + WebKit2GTK resolved via pkg-config
if(UNIX AND NOT APPLE)
    find_package(PkgConfig REQUIRED)
    pkg_check_modules(GTK3    REQUIRED IMPORTED_TARGET gtk+-3.0)
    pkg_check_modules(WEBKIT2 QUIET    IMPORTED_TARGET webkit2gtk-4.1)
    if(NOT WEBKIT2_FOUND)
        pkg_check_modules(WEBKIT2 REQUIRED IMPORTED_TARGET webkit2gtk-4.0)
    endif()
endif()

# ---------------------------------------------------------------------------
# Embed frontend HTML at build time
# ---------------------------------------------------------------------------
set(FRONTEND_HTML  "${CMAKE_SOURCE_DIR}/src/frontend.html")
set(GENERATED_DIR  "${CMAKE_CURRENT_BINARY_DIR}/generated")
set(EMBEDDED_H     "${GENERATED_DIR}/frontend_html.h")

file(MAKE_DIRECTORY "${GENERATED_DIR}")

add_custom_command(
    OUTPUT  "${EMBEDDED_H}"
    COMMAND ${Python3_EXECUTABLE}
            "${CMAKE_SOURCE_DIR}/cmake/embed_html.py"
            "${FRONTEND_HTML}"
            "${EMBEDDED_H}"
    DEPENDS "${FRONTEND_HTML}" "${CMAKE_SOURCE_DIR}/cmake/embed_html.py"
    COMMENT "Embedding frontend HTML..."
    VERBATIM
)

add_custom_target(embed_frontend DEPENDS "${EMBEDDED_H}")

# ---------------------------------------------------------------------------
# Executable
# ---------------------------------------------------------------------------
add_executable(${PROJECT_NAME}
    src/main.cpp
)

add_dependencies(${PROJECT_NAME} embed_frontend)

target_include_directories(${PROJECT_NAME} PRIVATE
    include
    "${GENERATED_DIR}"
)

target_link_libraries(${PROJECT_NAME} PRIVATE webview::core)

if(APPLE)
    # Bundle the executable into a proper .app
    set_target_properties(${PROJECT_NAME} PROPERTIES
        MACOSX_BUNDLE                 TRUE
        MACOSX_BUNDLE_INFO_PLIST      "${CMAKE_SOURCE_DIR}/macos/Info.plist"
        MACOSX_BUNDLE_BUNDLE_NAME     "jrnl"
        MACOSX_BUNDLE_BUNDLE_VERSION  "${PROJECT_VERSION}"
        MACOSX_BUNDLE_SHORT_VERSION_STRING "0.1"
        MACOSX_BUNDLE_GUI_IDENTIFIER  "com.local.jrnl"
    )

    # Ad-hoc code signature — required for WKWebView to work outside a terminal
    find_program(CODESIGN codesign REQUIRED)
    add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
        COMMAND ${CODESIGN} --force --deep --sign - "$<TARGET_BUNDLE_DIR:${PROJECT_NAME}>"
        COMMENT "Ad-hoc signing jrnl.app..."
    )
endif()

if(UNIX AND NOT APPLE)
    target_link_libraries(${PROJECT_NAME} PRIVATE
        PkgConfig::GTK3
        PkgConfig::WEBKIT2
    )
endif()
