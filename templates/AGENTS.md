# MiniTools extension project instructions

These instructions apply to every AI-assisted task in this project.

## Source of truth

Before planning or changing an extension, read:

- https://github.com/LuisGil15/MiniTools-Plugins/blob/main/docs/creating-extensions.md
- https://github.com/LuisGil15/MiniTools-Plugins/blob/main/docs/connecting-apps.md
- https://github.com/LuisGil15/MiniTools-Plugins/blob/main/schemas/plugin-manifest.schema.json
- https://github.com/LuisGil15/MiniTools-Plugins/blob/main/schemas/notch-connect-event.draft.schema.json

Do not invent MiniTools APIs, capabilities, permissions, transports, or package
behavior that these documents do not define.

## Platform status

- MiniTools 1.0.x activates only reviewed first-party runtimes already shipped
  inside the signed host app.
- A package with a new plugin identifier is a proposal until MiniTools includes
  a compatible runtime.
- Notch Connect is a Developer Preview and has no stable public endpoint yet.
- Never use the private Agent Pulse/Codex receiver as an integration API.
- MiniTools owns notch geometry, windows, animation, permissions, priority, and
  system consent prompts.

## Required workflow

1. Decide whether the feature is a full extension or an app integration.
2. Define one focused user problem and explicit non-goals.
3. Specify compact, expanded, inactive, loading, empty, error, and permission
   states before writing implementation code.
4. Request only contract-v1 capabilities required by visible behavior.
5. Document storage, retention, uninstall, network, privacy, timeout, and crash
   behavior.
6. Validate manifests and events against the published schemas.
7. Separate current MiniTools support from future host or SDK work.

## Safety and privacy

- Never place secrets, access tokens, prompts, source code, terminal output,
  personal data, analytics payloads, or full logs in notch events.
- Destructive actions require explicit user intent and confirmation.
- Keep the compact island glanceable and avoid repeated forced openings.
- Do not add capabilities merely because they may be useful later.
- Do not replace a published package version in place.

## Completion criteria

A change is complete only when its JSON validates, capability use is justified,
privacy and removal behavior are documented, current limitations remain clear,
and the compact and expanded experiences have testable acceptance criteria.
