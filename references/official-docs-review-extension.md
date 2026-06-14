# Official Docs Review Extension

Use this during review when platform, framework, SDK, host-integration, system API, or platform-design constraints were relevant during implementation.

## Review Checks

Verify:

1. the implementation identified the relevant platform, framework, SDK, host, or UI system
2. official docs check was performed when the task required it
3. lifecycle requirements were followed
4. threading-model requirements were followed
5. permission, security, or host requirements were followed
6. resource-loading, configuration, or control-template rules were followed
7. deprecated or discouraged APIs were not used without justification
8. compatibility notes and known limitations were considered
9. UI-facing work follows platform design guidelines, or the deviation is explicitly justified
10. tests or manual acceptance steps cover the official constraints that mattered

## Blocking Conditions

Flag review blockers when:

- platform-related code changed without required official docs check
- an officially discouraged or deprecated API is used without a defensible reason
- lifecycle, threading, permission, template, or host requirements are violated
- UI work drifts from platform design guidelines without a documented reason
- repeated failed bug-fix work still skips official-docs backchecking
