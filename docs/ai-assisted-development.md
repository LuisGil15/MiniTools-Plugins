# Build a MiniTools extension with an AI assistant

An AI assistant can help turn an idea into a clear extension proposal, manifest,
and integration lifecycle. It still needs accurate product context: without it,
the assistant may invent APIs or claim that MiniTools can load third-party code
that the current release does not support.

## Before you start

Give the assistant these files or links as source material:

1. [Creating extensions](./creating-extensions.md)
2. [Connecting apps](./connecting-apps.md)
3. [Plugin manifest schema](../schemas/plugin-manifest.schema.json)
4. [Notch Connect event draft](../schemas/notch-connect-event.draft.schema.json)

Tell the assistant which path you need:

- **Extension:** a dedicated compact and expanded tab inside MiniTools.
- **App integration:** an existing app publishes short-lived status to the
  notch without owning a MiniTools tab.

> [!IMPORTANT]
> MiniTools 1.0.x only installs reviewed first-party runtimes already shipped in
> the host app. An AI-generated manifest with a new identifier is a proposal,
> not an immediately installable plugin. Notch Connect is also a Developer
> Preview until a future MiniTools release exposes the public bridge.

## Recommended workflow

Use one prompt at a time. Review the output before continuing so a wrong product
assumption does not propagate into code or package metadata.

### 1. Shape the idea

Start with the [extension designer prompt](../prompts/extension-designer.md).
It asks the assistant to decide whether the idea belongs in an extension or an
app integration, then defines compact, expanded, inactive, and error states.

If the assistant works directly inside a project, copy
[`templates/AGENTS.md`](../templates/AGENTS.md) into the project root. Coding
agents that support repository instructions will then receive the MiniTools
contract and safety constraints on every task.

### 2. Prepare the contract

For an extension, ask the assistant to produce a contract-v1 manifest and a
capability justification. For an existing app, use the
[Notch Connect prompt](../prompts/notch-connect-integration.md) to design a
versioned event lifecycle and example payloads.

### 3. Review before submitting

Run the [security and contract review prompt](../prompts/security-review.md)
with the proposed manifest, UX specification, and event examples. The reviewer
should identify unsupported APIs, excessive capabilities, private data, and
notch behavior that could interrupt the user.

### 4. Validate deterministic files

AI output is not validation. Save JSON files and run:

```bash
python3 scripts/validate.py
```

For a new proposal that is not yet part of the catalog, also validate the
manifest against [`plugin-manifest.schema.json`](../schemas/plugin-manifest.schema.json)
with a JSON Schema 2020-12 validator.

### 5. Submit for review

Use the final specification to open either a
[plugin proposal](https://github.com/LuisGil15/MiniTools-Plugins/issues/new?template=plugin-proposal.yml)
or an
[app integration proposal](https://github.com/LuisGil15/MiniTools-Plugins/issues/new?template=app-integration.yml).

## One-shot prompt

Use this when the idea is still rough and you want one complete first draft:

```text
Help me design a MiniTools extension or app integration for macOS.

Idea: [DESCRIBE THE USER PROBLEM]
Target users: [WHO NEEDS IT]
Existing app, if any: [APP NAME AND BUNDLE IDENTIFIER OR "NONE"]
Data involved: [LOCAL DATA, NETWORK SERVICES, OR "NONE"]

Treat the MiniTools developer documentation and JSON schemas I provide as the
only source of truth. Do not invent host APIs, capabilities, permissions, or
installation behavior.

Important constraints:
- MiniTools 1.0.x only enables reviewed first-party runtimes already included
  in the signed host.
- Unknown plugin IDs are proposals and are not installable yet.
- Notch Connect is a Developer Preview, not a stable endpoint.
- MiniTools owns notch geometry, animation, windows, permissions, and priority.
- Request the minimum capabilities and never include secrets, prompts, source
  code, terminal output, or full logs in user-visible events.

First decide whether this should be a full extension or an app integration and
explain the choice. Then produce:
1. A one-sentence product promise.
2. Compact, expanded, inactive, loading, empty, and error states.
3. Primary and destructive actions, including confirmations.
4. Required capabilities with a reason for each.
5. Local storage, network, privacy, and removal behavior.
6. A valid sample manifest or Notch Connect event lifecycle.
7. What works in MiniTools 1.0.x versus what requires a future host release.
8. A testing checklist and GitHub proposal draft.

Ask only for information that materially changes the design. Mark assumptions
explicitly and do not write implementation code until the contract is coherent.
```

## What a good AI-assisted proposal contains

- One focused job instead of a collection of unrelated tools.
- A useful compact state that does not become a second full-size window.
- Clear behavior when there is no activity.
- Minimal capabilities and an explicit privacy model.
- Stable identifiers and semantic versions.
- A manifest or event sequence that validates against the published schema.
- A visible separation between current support and future platform work.
