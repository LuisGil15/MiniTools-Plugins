# Prompt: design a MiniTools extension

Copy this prompt into your AI assistant and replace the bracketed values.

```text
You are designing a focused extension for MiniTools, a macOS island that lives
around the notch.

Extension idea: [IDEA]
User problem: [PROBLEM]
Target users: [USERS]
Relevant apps or services: [APPS, SERVICES, OR "NONE"]
Data involved: [DATA OR "NONE"]

Use the attached MiniTools extension guide and plugin-manifest JSON Schema as
the source of truth. Do not invent capabilities or host APIs.

Platform constraints:
- MiniTools 1.0.x only activates reviewed runtimes already shipped in the host.
- A new manifest is a proposal until MiniTools includes its runtime.
- MiniTools owns the notch window, geometry, animations, permissions, tab bar,
  prioritization, and system prompts.
- The extension must declare only capabilities from contract version 1.

Work in this order:
1. Decide whether the idea is best as a MiniTools extension or a Notch Connect
   app integration. Explain the decision in three sentences or fewer.
2. Define one product promise and three non-goals.
3. Specify compact, expanded, inactive, loading, empty, error, and permission
   states. Keep the compact state glanceable with at most one primary action.
4. List every user action. Mark destructive actions and their confirmation.
5. Map required capabilities to concrete behavior and remove any capability
   that is not essential.
6. Document saved data, retention, uninstall behavior, network destinations,
   and exactly which fields leave the Mac.
7. Produce a contract-v1 manifest that validates against the provided schema.
8. Separate behavior available in MiniTools 1.0.x from host work required in a
   future release.
9. Finish with accessibility, failure-mode, and test checklists.

Do not write Swift implementation code yet. Ask a question only if the missing
answer would materially change the contract; otherwise state a safe assumption.
```
