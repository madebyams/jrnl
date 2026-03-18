# Contributing to jrnl.

Thanks for taking the time. jrnl. is intentionally small — contributions that keep it that way are most welcome.

---

## Ground rules

- **No network calls, ever.** The app must remain fully offline. No external scripts, no CDN fonts, no analytics.
- **No new dependencies without a strong reason.** The current dep-count is 1 (webview). Opening a merge request that adds a framework will require very convincing justification.
- **Respect the aesthetic.** Warm beige, monospaced text, no chrome. UI changes should preserve the minimal feel.

---

## Development setup

### Prerequisites

| Tool | Version |
|------|---------|
| macOS | 13+ |
| Xcode Command Line Tools | any recent |
| CMake | ≥ 3.22 |
| Conan | ≥ 2.0 |
| Python | ≥ 3.8 |

```bash
brew install cmake conan python
```

### First build

```bash
git clone git@git.anothersimplecoder.de:anotherSimpleCoder/jrnl.git
cd jrnl

cmake -B cmake-build-debug -DCMAKE_BUILD_TYPE=Debug
cmake -B cmake-build-debug -DCMAKE_BUILD_TYPE=Debug   # second pass after Conan generates toolchain
cmake --build cmake-build-debug --target jrnl
open cmake-build-debug/jrnl.app
```

### Iterating on the UI

The entire frontend lives in `src/frontend.html`. Edit it, rebuild, and relaunch:

```bash
cmake --build cmake-build-debug --target jrnl && open cmake-build-debug/jrnl.app
```

The embed script (`cmake/embed_html.py`) re-runs automatically when `frontend.html` changes.

### Iterating on the C++ host

Edit `src/main.cpp`, then rebuild as above. The WebView initialisation is in `main()`.

---

## Submitting changes

1. **Fork** the repo and create a branch from `main`:
   ```bash
   git checkout -b fix/my-fix
   ```

2. **Make your changes.** Keep commits focused — one logical change per commit.

3. **Test locally** by building in Release mode and confirming the `.app` launches and functions correctly:
   ```bash
   cmake -B cmake-build-release -DCMAKE_BUILD_TYPE=Release
   cmake -B cmake-build-release -DCMAKE_BUILD_TYPE=Release
   cmake --build cmake-build-release --target jrnl
   open cmake-build-release/jrnl.app
   ```

4. **Open a Merge Request** against `main`. Describe what the change does and why.

---

## Code style

- **C++17**, formatted consistently with the existing code.
- No raw `new`/`delete` — use RAII.
- Keep `main.cpp` short. Logic that doesn't belong in `main()` goes in a header under `include/jrnl/`.
- HTML/CSS: 2-space indent, no external resources.

---

## Versioning

jrnl. follows [Semantic Versioning](https://semver.org). Releases are tagged `vMAJOR.MINOR.PATCH` on `main`. The version number lives in `CMakeLists.txt` (`project(jrnl VERSION …)`).

---

## Reporting bugs

Open an issue with:
- macOS version
- Reproduction steps
- What you expected vs. what happened
