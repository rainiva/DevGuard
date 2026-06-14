# Official Docs Check

## Metadata

- Layer: core
- Load level: metadata, summary, full
- Use when: platform, framework, SDK, system API, host integration, control template, ORM, or official design-guideline constraints may govern the implementation.
- Risk tags: `official_docs_required`, `platform_api`, `framework_lifecycle`, `threading_model`, `sdk_usage`, `control_template`, `host_compatibility`, `deprecated_api`, `platform_design`

## Summary

Before impact analysis, confirm the official platform or framework constraints that define how the implementation is allowed to behave. CodeGraph explains how the project is currently written. Official Docs Check explains what the platform or framework officially requires.

## Full Rule

### Relationship To Other Stages

Treat these stages differently:

- Project understanding: understand the current code structure and entry points.
- Official Docs Check: confirm the official platform, framework, SDK, host, or design constraints that govern the implementation.
- Impact analysis: judge what this specific change could affect.
- Task Contract: freeze what this task is allowed to change and how it will be accepted.

Do not begin impact analysis when official docs check is required but missing.

### Trigger Conditions

Default to required when the task involves any of these:

1. using or modifying a platform API
2. using or modifying system capabilities
3. using or modifying control templates, lifecycle behavior, or threading models
4. modifying permissions, filesystems, registry, services, installers, or startup behavior
5. modifying Office, WPS, browser, mobile, desktop-plugin, or host-integration behavior
6. using or modifying a third-party SDK, AI SDK, ORM, or UI framework
7. repeated failed bug-fix attempts
8. compatibility-sensitive work
9. performance-sensitive work on framework or platform paths
10. platform behavior that does not match expectations
11. refactoring platform-related code
12. using an unfamiliar or uncertain API
13. UI tasks that should follow target-platform design guidelines

### Usually Skip Conditions

Usually skip only when the task is clearly one of these:

1. documentation-only work
2. a tiny local text or copy tweak
3. pure business-logic changes that do not touch platform, framework, SDK, UI-host, or system constraints
4. pure consultation with no code or behavior change

### Required Sources

Prefer these sources in order:

1. official documentation
2. official API reference
3. official samples
4. official design guidelines
5. official migration guides
6. official compatibility notes
7. official known issues or limitations
8. official deprecated API or breaking-change notes

Load these sources progressively. Start from the exact platform, API, control, SDK, host, or design surface identified by project understanding. Do not query broad official documentation packs or unrelated platform areas just because the task is platform-sensitive.

### Required Questions

Official docs check must answer:

1. which platform, framework, SDK, host, or UI system is involved
2. which lifecycle requirements matter
3. which threading-model requirements matter
4. which permission or security requirements matter
5. which resource-loading or configuration requirements matter
6. which control-template or named-part requirements matter
7. which compatibility or host constraints matter
8. which performance guidance matters
9. which deprecated APIs or breaking changes matter
10. which official design guidelines matter for UI-facing work
11. which constraints must enter the Task Contract
12. which tests or manual checks must prove compliance

### UI Design Priority

For UI design, UI implementation, component implementation, interaction changes, layout, navigation, dialog, state-feedback, icon, motion, or accessibility work, confirm the target platform's official design guidelines by default.

Do not drift away from platform design conventions without an explicit reason.

Allowed reasons for deviation include:

1. the project already uses a deliberate cross-platform design system
2. the project already has a mature UI style guide
3. the product needs a strong branded or creative visual identity
4. default platform controls cannot satisfy the product experience
5. the UI must work across multiple hosts
6. the user explicitly asked for a specific visual style

When deviation is allowed, explain:

1. what is being deviated from
2. why the deviation is needed
3. what replacement basis is used instead
4. whether accessibility is affected
5. whether platform consistency is affected
6. whether extra UI review is required

### Bug-Fix Counter-Proof

If a bug touches platform behavior, control behavior, system APIs, SDK calls, or host integration, root-cause analysis must include the counter-proof question: "Does the current implementation violate official platform or framework requirements?"

Check:

1. wrong lifecycle usage
2. wrong threading-model usage
3. wrong async, dispatcher, or UI-thread usage
4. wrong resource-loading mechanism
5. wrong control-template or required-part usage
6. deprecated API usage
7. missing permission or compatibility requirements
8. known platform limitations that already explain the symptom

### Fallback Rule

If official sources are unavailable, say exactly:

`无法访问官方资料，已使用项目现有实现、源码注释、测试和稳定实践作为降级依据。`

Do not pretend the fallback is equivalent to confirmed official guidance.

### Output Depth

#### Summary

Use `Official Docs Check Summary` from `references/report-templates.md`.

Default to this when the check is required but outward output should remain compact.

#### Focused Expansion

Use `Official Docs Check Summary` plus `Official Docs Focused Expansion`.

Default to this when only the risky official constraints need outward explanation.

#### Full

Use `Official Docs Check Report` from `references/report-templates.md`.

Use this only when one of these is true:

1. the user explicitly asks for detailed, verbose, debug, or audit output
2. the task is a formal evidence-capture or forward-testing pass that explicitly requires the canonical full template

### Output Discipline

- Default outward output should still stay minimal.
- Do not dump long official excerpts into normal-task output.
- Do not load or summarize unrelated official docs. Keep the check scoped to the surfaces that can actually constrain this task.
- Surface official-docs findings outward only when risk, anomaly, or explicit detailed mode requires it.
- Except for headings, labels, keywords, paths, and code identifiers, write outward report prose in Chinese.
