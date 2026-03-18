#pragma once

#include <filesystem>
#include <stdexcept>
#include <string>

#if defined(_WIN32)
    #include <windows.h>
#elif defined(__APPLE__)
    #include <mach-o/dyld.h>
    #include <limits.h>
#else
    #include <unistd.h>
    #include <limits.h>
#endif

namespace jrnl {

// Returns the directory that contains the running executable.
inline std::filesystem::path binary_dir()
{
#if defined(_WIN32)
    wchar_t buf[MAX_PATH];
    GetModuleFileNameW(nullptr, buf, MAX_PATH);
    return std::filesystem::path(buf).parent_path();
#elif defined(__APPLE__)
    char buf[PATH_MAX];
    uint32_t size = sizeof(buf);
    if (_NSGetExecutablePath(buf, &size) != 0)
        throw std::runtime_error("Could not resolve executable path");
    return std::filesystem::canonical(buf).parent_path();
#else
    char buf[PATH_MAX];
    ssize_t len = readlink("/proc/self/exe", buf, sizeof(buf) - 1);
    if (len == -1)
        throw std::runtime_error("Could not resolve executable path");
    buf[len] = '\0';
    return std::filesystem::path(buf).parent_path();
#endif
}

// Returns the path to the frontend/ directory, co-located with the binary.
inline std::string frontend_dir()
{
    return (binary_dir() / "frontend").string();
}

} // namespace jrnl
