# WPF Scrollbar Bug Playbook

## Metadata

- Issue class: WPF scrollbar behavior, visibility, template, thumb, or track defect
- Load level: metadata, summary, full

## Summary

Use only when the concrete issue involves WPF scrollbar behavior or rendering.

## Full Rule

Check:

1. `ScrollViewer` ownership
2. scrollbar visibility mode
3. template parts such as track and thumb
4. style/resource lookup order
5. content extent versus viewport size
6. keyboard, wheel, drag, and touch behavior where relevant
