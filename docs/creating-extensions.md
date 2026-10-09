# Create a MiniTools extension

This guide describes the public extension contract and the review path for
adding a focused tool to the MiniTools island.

## Support status

| Capability | MiniTools 1.0.x | Developer Preview |
| --- | --- | --- |
| Install a reviewed `.minitoolplugin` manifest | Supported | — |
| Enable a first-party runtime shipped in MiniTools | Supported | — |
| Submit a new extension proposal | Supported | — |
| Load third-party Swift or SwiftUI code | Not supported | Planned behind an isolated process boundary |
| Publish an unreviewed plugin ID to the store | Not supported | Planned with signing and review |

Today, a package is a cataloged manifest that enables a runtime already
present in the notarized MiniTools host. Creating a manifest alone does not add
executable behavior. MiniTools 1.0.x rejects unknown runtime identifiers with
`unsupportedPlugin`.

## 1. Define one focused job

An extension should solve one clear problem and work in both island sizes:

- **Compact:** glanceable state and one safe primary action.
- **Expanded:** configuration, history, or secondary actions.
- **Inactive:** no decorative controls or background work without a purpose.

MiniTools owns the window, notch geometry, transitions, permissions, and tab
navigation. Extensions should not create another floating notch window.

## 2. Choose a stable identifier

Use reverse-DNS notation and never reuse an ID for a different extension:

```text
com.yourcompany.minitools.extension-name
```

The tab ID should be short, stable, and unique within the package.

## 3. Request the minimum capabilities

Contract version 1 currently recognizes:

| Capability | Purpose |
| --- | --- |
| `applicationLaunch` | Launch a user-selected application |
| `applicationDiscovery` | Resolve application metadata and icons |
| `notifications` | Present user-visible completion or attention alerts |
| `processInspection` | Read local process metadata |
| `processTermination` | Terminate a process after an explicit user action |
| `screenshotEvents` | Observe newly created screenshots |
| `fileDragAndDrop` | Expose files through native drag and drop |
| `keepAwake` | Create a macOS power assertion |
| `terminalSession` | Run an interactive local terminal session |

Capabilities are declarations, not automatic permission grants. MiniTools still
owns consent prompts and sensitive actions.

## 4. Create the manifest

Save a flat UTF-8 JSON file using the `.minitoolplugin` extension:

```json
{
  "id": "com.example.minitools.build-monitor",
  "name": "Build Monitor",
  "version": "0.1.0",
  "minimumHostVersion": "1.0.3",
  "contractVersion": "1",
  "systemImage": "hammer.fill",
  "capabilities": ["notifications"],
  "tabs": [
    {
      "id": "build-monitor",
      "title": "Builds",
      "systemImage": "hammer.fill",
      "presentation": "both"
    }
  ],
  "priority": 10,
  "repositoryURL": "https://github.com/example/build-monitor"
}
```

Use an SF Symbol name for `systemImage`. `presentation` accepts `compact`,
`expanded`, or `both`. Validate the file against
[`plugin-manifest.schema.json`](../schemas/plugin-manifest.schema.json).

Run the repository validator before submitting:

```bash
python3 scripts/validate.py
```

## 5. Package and verify

Rename the JSON file and calculate its checksum:

```bash
mv manifest.json BuildMonitor-0.1.0.minitoolplugin
shasum -a 256 BuildMonitor-0.1.0.minitoolplugin
```

Do not replace released bytes in place. Any change to the package requires a
new semantic version and checksum.

## 6. Submit the extension

Open a [plugin proposal](https://github.com/LuisGil15/MiniTools-Plugins-Distribution/issues/new?template=plugin-proposal.yml)
with:

1. The user problem and why it belongs in the notch.
2. Compact and expanded behavior.
3. Every requested capability and its reason.
4. A sample manifest and screenshots or a short interaction video.
5. Data storage, network access, and privacy behavior.

Accepted proposals currently require a MiniTools host release that adds the
reviewed runtime before the package can be installed. The future isolated SDK
will remove that host-release requirement for compatible third-party plugins.

## Review checklist

- The compact view remains understandable at a glance.
- Destructive actions require an explicit confirmation.
- The extension stays idle when its feature is inactive.
- Saved data has a documented location and removal behavior.
- Network destinations and transmitted fields are documented.
- The manifest requests no unused capability.
- The package version, checksum, and catalog entry agree.
