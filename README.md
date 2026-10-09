<div align="center">

# MiniTools Extensions

### Add only the tools you want to your macOS island.

[![Catalog schema](https://img.shields.io/badge/catalog-v1-0A84FF)](./index.json)
[![MiniTools](https://img.shields.io/badge/requires-MiniTools_1.0%2B-black)](https://github.com/LuisGil15/MiniTools)
[![Packages](https://img.shields.io/badge/extensions-6-30D158)](#extension-gallery)

[Get MiniTools](https://github.com/LuisGil15/MiniTools/releases/latest) ·
[Browse packages](./packages) ·
[View the catalog](./index.json) ·
[Developer guides](#build-with-minitools)

</div>

This repository is the official distribution catalog for MiniTools extensions.
Each extension adds one focused capability while MiniTools keeps control of the
notch, animations, permissions, and shared state.

## Extension gallery

| Extension | What it adds | Best for |
| --- | --- | --- |
| **Agent Pulse** | Codex activity, help requests, completion alerts, and an edge pulse | Following AI work without changing windows |
| **Caffeine** | Timed or indefinite keep-awake sessions with a notch indicator | Presentations, downloads, and long-running jobs |
| **Launchpad** | A drag-and-drop grid for favorite applications | Opening everyday apps from the notch |
| **Mini Terminal** | A real interactive login-shell PTY | Quick commands without leaving the current app |
| **Ports** | Local TCP/UDP listener inspection and explicit process termination | Finding and freeing development ports |
| **Screenshot Board** | Automatic capture collection and native drag-and-drop | Moving recent screenshots between apps |

See [the complete extension details](./extensions/README.md), including the
capabilities each package requests.

## Build with MiniTools

MiniTools is opening its extension surface in stages. The developer portal
separates what works in the current release from contracts that are still in
Developer Preview:

- [Create a MiniTools extension](./docs/creating-extensions.md) — manifest,
  capabilities, packaging, validation, and the current submission flow.
- [Connect an app to the notch](./docs/connecting-apps.md) — proposed lifecycle
  events, privacy rules, UX behavior, and the integration roadmap.
- [Build with an AI assistant](./docs/ai-assisted-development.md) — a guided
  workflow and copy-ready prompts that keep generated proposals inside the
  current MiniTools contract.
- [Plugin manifest JSON Schema](./schemas/plugin-manifest.schema.json) — the
  machine-readable contract used by `.minitoolplugin` packages.
- [Notch Connect event draft](./schemas/notch-connect-event.draft.schema.json) —
  the proposed event envelope for external apps.

> [!IMPORTANT]
> MiniTools 1.0.x only enables reviewed first-party runtimes already included
> in the signed host app. It does not load arbitrary third-party executable
> code. External plugin IDs and the Notch Connect API require a future MiniTools
> release; the guides clearly mark those steps as Developer Preview.

## Install

### From MiniTools

1. Open **MiniTools → Settings → Extension Store**.
2. Choose an extension and click **Install**.
3. Its tab appears immediately; no app restart is required.

### From a file

1. Download a `.minitoolplugin` file from [`packages/`](./packages).
2. Open **MiniTools → Settings → Installed Plugins**.
3. Click **Install from File…** and select the package.

## How the catalog works

[`index.json`](./index.json) is the machine-readable source of truth. Every
entry has a stable identifier, semantic version, minimum MiniTools version,
HTTPS download URL, SHA-256 checksum, and requested capabilities.

MiniTools downloads the selected package, verifies its published checksum,
validates the manifest and host compatibility, and only then installs it in:

```text
~/Library/Application Support/MiniTools/Plugins/
```

The current first-party packages are manifests that enable runtimes already
shipped inside the signed and notarized MiniTools app. Arbitrary third-party
code loading is not enabled yet.

Validate the catalog, package metadata, checksums, and Developer Preview event
examples with only Python's standard library:

```bash
python3 scripts/validate.py
```

## Publishing rules

- Never replace a released package in place; publish a new semantic version.
- Keep the checksum in `index.json` synchronized with the exact package bytes.
- Request only capabilities declared by the package manifest.
- Keep download URLs on HTTPS and preserve older packages for rollback.

The extension SDK and isolated third-party runtime are planned. Until that
boundary is ready, this catalog contains first-party extensions only.
