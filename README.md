# MiniTools Plugins Distribution

Private catalog for packaged MiniTools plugins while the plugin runtime and
signing policy are being finalized.

## Catalog contract

`index.json` is the source of truth for available plugin packages. Every entry
must include a stable plugin identifier, semantic version, compatible host
version, download URL, checksum, and requested capabilities.

Packages use the `.minitoolplugin` extension and should be attached to a GitHub
release. MiniTools must validate the manifest and SHA-256 checksum before
installing or replacing a package.

## Safety rules

- Do not publish a package without a valid `manifest.json`.
- Do not replace an existing version in place.
- Do not grant capabilities that are absent from the package manifest.
- Keep the repository private until package signing and runtime isolation are
  complete.
