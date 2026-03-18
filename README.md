# jrnl.

A minimal, distraction-free journaling app for macOS.
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

## Building

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

## Running

Double-click `jrnl.app` in Finder, or:

```bash
open cmake-build-release/jrnl.app
```

To install system-wide:

```bash
cp -r cmake-build-release/jrnl.app /Applications/
```

## Keyboard shortcuts

| Shortcut | Action |
|----------|--------|
| `Cmd+A` | Select all text |

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

- **[webview](https://github.com/webview/webview)** — thin cross-platform wrapper around WKWebView (macOS)
- **CMake + Conan** — build system and C++ package management
- **Vanilla HTML/CSS/JS** — the entire UI in one file, zero framework overhead

## License

MIT — see [LICENSE](LICENSE).
