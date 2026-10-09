# Connect an app to the MiniTools notch

Notch Connect is the proposed event contract for apps that want to surface
short-lived progress, attention, and completion states in MiniTools without
becoming a full island extension.

> [!WARNING]
> The generic Notch Connect endpoint is not available in MiniTools 1.0.x. The
> schema in this repository is a Developer Preview for feedback and integration
> planning. Do not depend on the private Agent Pulse/Codex receiver; it can
> change without notice and is not an app integration API.

## When to use an app integration

Use Notch Connect when your app already owns its interface and only needs to
publish status. Build a full extension when the user should interact with a
dedicated compact or expanded MiniTools tab.

Good integration events are:

- a build, export, upload, or AI task started;
- progress changed meaningfully;
- the app needs a decision or permission;
- the task completed, failed, or was cancelled.

Do not mirror ordinary notifications, logs, chat messages, or rapidly changing
telemetry into the notch.

## Proposed connection flow

1. The user enables your app in **MiniTools → Settings → Integrations**.
2. MiniTools verifies the app identity and issues a revocable local credential.
3. Your app sends versioned events through the authenticated local bridge.
4. MiniTools applies rate limits, privacy filtering, and presentation priority.
5. The user can pause or revoke the integration at any time.

The planned bridge is local-only. It must not accept remote-network traffic,
and credentials must not be embedded in source code or transmitted off-device.

## Event lifecycle

Each activity has a stable `activity.id`. Send `activity.started` once, then
updates using the same ID, followed by exactly one terminal event.

```text
activity.started
      │
      ├── activity.updated ── activity.updated
      │
      ├── activity.needsAttention
      │
      └── activity.completed | activity.failed | activity.cancelled
```

Example payload:

```json
{
  "schemaVersion": 1,
  "source": {
    "bundleIdentifier": "com.example.builder",
    "name": "Builder"
  },
  "event": "activity.updated",
  "activity": {
    "id": "release-184",
    "title": "Building release",
    "detail": "Signing the macOS app",
    "progress": 72,
    "systemImage": "hammer.fill",
    "accentColor": "#0A84FF"
  },
  "timestamp": "2026-10-08T20:15:00Z",
  "expiresInSeconds": 900
}
```

See the complete
[`notch-connect-event.draft.schema.json`](../schemas/notch-connect-event.draft.schema.json)
and [sample lifecycle](../examples/notch-connect-events.json).

## Presentation rules

| Event | Collapsed island | Expanded island |
| --- | --- | --- |
| `activity.started` | Optional edge pulse | Activity appears in the integration list |
| `activity.updated` | Pulse continues; no forced opening | Progress and detail update in place |
| `activity.needsAttention` | Island may open with a concise alert | Shows the app and required action |
| `activity.completed` | Brief completion state, then dismisses | Moves to recent activity |
| `activity.failed` | Brief error state without sensitive logs | Shows a safe error summary |
| `activity.cancelled` | Stops the pulse silently | Marks the activity cancelled |

MiniTools decides when to open, collapse, or suppress the island so one app
cannot monopolize the notch.

## Privacy and safety

- Send display-ready summaries, never prompts, source code, terminal output,
  credentials, access tokens, or full logs.
- Keep `title` and `detail` short; the schema enforces maximum lengths.
- Use an opaque activity ID that does not contain personal information.
- Never use the notch as a background analytics channel.
- Declare whether your app uses the network independently of MiniTools.
- Treat completion callbacks as best-effort UI state, not durable job storage.

## Propose an integration

Open an [app integration proposal](https://github.com/LuisGil15/MiniTools-Plugins-Distribution/issues/new?template=app-integration.yml)
and include your bundle identifier, event lifecycle, example payloads, expected
event frequency, and the information users will see.

Feedback on the draft will determine the transport, registration flow, and
compatibility guarantees before Notch Connect is marked stable.
