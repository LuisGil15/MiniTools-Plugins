# Prompt: design a Notch Connect app integration

Copy this prompt into your AI assistant and replace the bracketed values.

```text
Help me prepare a Developer Preview Notch Connect proposal for MiniTools.

App name: [APP NAME]
macOS bundle identifier: [BUNDLE IDENTIFIER]
Activity to surface: [BUILD, EXPORT, UPLOAD, AI TASK, OR OTHER]
Typical duration: [DURATION]
Expected update frequency: [FREQUENCY]
User attention conditions: [CONDITIONS]

Use the attached MiniTools app-integration guide and Notch Connect draft JSON
Schema as the only source of truth. The public bridge is not implemented in
MiniTools 1.0.x, so label all transport and registration work as future host
work. Never depend on the private Agent Pulse/Codex receiver.

Produce:
1. A short explanation of why this should be an app integration rather than a
   full MiniTools extension.
2. One complete lifecycle using a stable activity ID: started, meaningful
   updates, optional needs-attention, and exactly one terminal event.
3. Valid JSON examples for every event used.
4. The collapsed and expanded island behavior for each event.
5. A rate-limit recommendation that avoids noisy or frame-by-frame updates.
6. A privacy table listing every field MiniTools receives and why it is needed.
7. Credential storage, user enablement, pause, and revocation expectations.
8. Timeout, app crash, duplicate-event, stale-event, and offline behavior.
9. A test checklist and a ready-to-paste GitHub integration proposal.

Do not include prompts, source code, terminal output, credentials, access
tokens, analytics payloads, or full logs in an event. Use display-ready titles
and details within the schema length limits.
```
