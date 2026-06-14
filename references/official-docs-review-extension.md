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
11. Context7 or equivalent tooling was scoped to the correct library, version, and API or control surface
12. high-risk tasks did not rely only on Context7 summaries when original official-doc verification was required
13. fallback or partial-official-guidance states were disclosed when official verification was incomplete
14. conflicts between official guidance, project behavior, and test results were resolved explicitly

## Blocking Conditions

Flag review blockers when:

- platform-related code changed without required official docs check
- an officially discouraged or deprecated API is used without a defensible reason
- lifecycle, threading, permission, template, or host requirements are violated
- UI work drifts from platform design guidelines without a documented reason
- repeated failed bug-fix work still skips official-docs backchecking
- a high-risk platform decision relies only on Context7 summary output without original official-doc or API-reference verification
- Context7 matched the wrong library or wrong version and still drove the implementation
- fallback official-docs evidence is treated as fully confirmed official guidance
