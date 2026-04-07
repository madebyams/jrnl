# jrnl.

A minimal, distraction-free journaling app for macOS and Windows.
No accounts. No cloud. No network calls. Your words never leave your machine.

---

## What it is

jrnl. is a single-window desktop app built around a plain text area. Open it, write, close it. That's it. The UI is a warm beige canvas with nothing between you and the text.

```
┌─────────────────────────────────┐
│            jrnl.                │
│                                 │
│  Write your thoughts here...    │
│                                 │
└─────────────────────────────────┘
```

## Privacy

- **Zero network access.** The frontend is a single HTML file embedded directly in the binary at compile time. There is no HTTP server, no external CDN, no analytics, no telemetry.
- **Nothing is persisted automatically.** Text lives only in memory while the app is open.

## Requirements

### macOS

| Tool | Version |
|------|---------|
| macOS | 13 Ventura or later |
| Xcode Command Line Tools | any recent |
| CMake | ≥ 3.22 |
| Conan | ≥ 2.0 |
| Python | ≥ 3.8 |

Install missing tools with [Homebrew](https://brew.sh):

```bash
brew install cmake conan python
```

### Windows

| Tool | Version |
|------|---------|
| Windows | 10 or later |
| Visual Studio | 2022 (MSVC v143) |
| CMake | ≥ 3.22 |
| Conan | ≥ 2.0 |
| Python | ≥ 3.8 |
| WebView2 SDK | any recent |

The WebView2 runtime ships with Windows 11 and recent Windows 10 updates. The SDK (headers + import lib) must be downloaded separately — the easiest way is via NuGet:

```powershell
nuget install Microsoft.Web.WebView2 -OutputDirectory C:\webview2-sdk
```

Then point CMake at the extracted folder with `-DWEBVIEW2_SDK_DIR` (see [Building — Windows](#windows-1) below).

## Building

### macOS

```bash
git clone git@git.anothersimplecoder.de:anotherSimpleCoder/jrnl.git
cd jrnl

# First configure (Conan downloads webview and generates the toolchain)
cmake -B cmake-build-release -DCMAKE_BUILD_TYPE=Release

# Second configure (needed once after Conan generates the toolchain)
cmake -B cmake-build-release -DCMAKE_BUILD_TYPE=Release

# Build
cmake --build cmake-build-release --target jrnl
```

The result is `cmake-build-release/jrnl.app` — a fully self-contained, ad-hoc signed macOS app bundle.

### Windows

```powershell
git clone git@git.anothersimplecoder.de:anotherSimpleCoder/jrnl.git
cd jrnl

# First configure — Conan downloads webview and generates the toolchain.
# Point WEBVIEW2_SDK_DIR at your extracted NuGet package root.
cmake -B cmake-build-release -DCMAKE_BUILD_TYPE=Release `
      -DWEBVIEW2_SDK_DIR="C:\webview2-sdk\microsoft.web.webview2.<version>"

# Second configure (needed once after Conan generates the toolchain)
cmake -B cmake-build-release -DCMAKE_BUILD_TYPE=Release `
      -DWEBVIEW2_SDK_DIR="C:\webview2-sdk\microsoft.web.webview2.<version>"

# Build — note: --config Release is required with the Visual Studio generator
cmake --build cmake-build-release --target jrnl --config Release
```

> **Note:** The `--config Release` flag is required when building on Windows.
> Visual Studio is a multi-config generator and defaults to **Debug** when the
> flag is omitted. Because Conan only installs the Release variant of the
> webview package, the compiler would not find `webview/webview.h` in a Debug
> build.

The result is `cmake-build-release/Release/jrnl.exe`.

## Running

### macOS

Double-click `jrnl.app` in Finder, or:

```bash
open cmake-build-release/jrnl.app
```

To install system-wide:

```bash
cp -r cmake-build-release/jrnl.app /Applications/
```

### Windows

```powershell
.\cmake-build-release\Release\jrnl.exe
```

## Keyboard shortcuts

### macOS

| Shortcut | Action |
|----------|--------|
| `Cmd+A` | Select all text |

### Windows

| Shortcut | Action |
|----------|--------|
| `Ctrl+A` | Select all text |

## Project structure

```
jrnl/
├── src/
│   ├── main.cpp          # Entry point — creates WebView, injects HTML
│   └── frontend.html     # The entire UI (embedded into the binary at build time)
├── cmake/
│   └── embed_html.py     # Build-time script: HTML → C++ string_view header
├── macos/
│   └── Info.plist        # macOS app bundle metadata
├── recipes/
│   └── webview/          # Local Conan recipe for webview 0.12.0
├── include/jrnl/
│   └── app.h             # Cross-platform binary-path helpers
├── conanfile.py          # C++ dependency manifest
└── CMakeLists.txt        # Build system
```

## Tech stack

- **[webview](https://github.com/webview/webview)** — thin cross-platform wrapper around WKWebView (macOS) / WebView2 (Windows)
- **CMake + Conan** — build system and C++ package management
- **Vanilla HTML/CSS/JS** — the entire UI in one file, zero framework overhead

## License

MIT — see [LICENSE](LICENSE).
