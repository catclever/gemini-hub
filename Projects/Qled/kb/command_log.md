# Qled Command Execution Log

| Command | Working Directory | Purpose |
| :--- | :--- | :--- |
| `swift build -c release && cp .build/release/Qled dist/Qled.app/Contents/MacOS/Qled && cp Info.plist dist/Qled.app/Contents/Info.plist && cp Sources/Qled/Resources/index.html dist/Qled.app/Contents/Resources/index.html && codesign --force --deep --sign - dist/Qled.app && /System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -f dist/Qled.app` | `/Users/kael/Projects/Qled` | Build release binary, assemble `dist/Qled.app` bundle, ad-hoc sign, and register `qled://` URL scheme with macOS LaunchServices |
