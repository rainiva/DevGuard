# Compatibility Impact Analysis

## Metadata

- Layer: extension
- Load level: metadata, summary, full
- Use when: platform, OS, browser, runtime, package, file format, API version, or backward compatibility may change.
- Risk tags: `compatibility`, `versioning`, `installation`, `dependency`, `degradation`

## Summary

Compatibility work asks whether old and new callers, environments, data, packages, or UI hosts can continue to coexist. It matters before migrations, installers, desktop UI changes, public contracts, and runtime upgrades.

## Full Rule

Check:

1. Supported and unsupported versions or hosts.
2. Backward-compatible contract expectations.
3. Upgrade and downgrade behavior.
4. Default behavior when the new path is unavailable.
5. Feature flag, fallback, or degradation needs.
6. Tests or manual checks across the affected compatibility matrix.
7. Official compatibility notes or host constraints when platform or SDK behavior is involved.

Block if a compatibility-sensitive change ships with no old-path, fallback, or migration story.
