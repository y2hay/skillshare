---
name: dogma-vault-organizer
description: Expert knowledge base organizer for maintaining ~/dogma vault structure, deduplication, and PARA compliance. Makes autonomous decisions on organization while escalating structural changes to user committee.
---

<skill>
<objective>
Maintain the integrity, clarity, and usability of the `~/dogma` knowledge base using the PARA methodology, ensuring it remains deduplicated, decluttered, and optimized for retrieval.
</objective>

<quick_start>
Follow the Weekly Organization Session: Audit `00_Inbox`, scan for duplicates, maintain internal links, and review `01_Projects` for archival. Execute autonomous cleanup immediately; escalate structural changes to the user committee.
</quick_start>

<success_criteria>
- `00_Inbox` remains under 20 items through regular processing
- Redundant and duplicate files are merged or removed
- All files are correctly categorized into PARA folders (Projects, Areas, Resources, Archive)
- Internal `[[WikiLinks]]` are functional and consistent across file moves
- Git history shows regular commits for all organizational changes
</success_criteria>

<authority_levels>
<autonomous_decisions>
- **Deduplication**: Merge identical content and consolidate drafts.
- **Organization**: Move files to correct PARA locations and update links.
- **Cleanup**: Remove empty files, archive completed projects, and process inbox.
- **Maintenance**: Fix broken links and add missing metadata (dates, tags).
</autonomous_decisions>

<committee_approval_required>
- **Structural**: Modifications to top-level PARA directory structure.
- **Consolidation**: Merging entire directories or large-scale restructuring.
- **Deletion**: Removing files with substantive content or bulk deletions (>10 files).
</committee_approval_required>
</authority_levels>

<para_method_compliance>
- **00_Inbox**: Temporary capture (process weekly).
- **01_Projects**: Time-bound initiatives with clear endpoints.
- **02_Areas**: Ongoing responsibilities (e.g., Homelab, Home Assistant).
- **03_Resources**: Reference materials and evergreen content.
- **04_Archive**: Completed or inactive work.
- **05_Attachments**: Media and binary files.
</para_method_compliance>

<file_naming_standards>
- **Format**: Human-readable, descriptive, kebab-case (e.g., `ARR-Stack-Comparison.md`).
- **Conventions**: Prefix by PARA category where appropriate for discoverability.
</file_naming_standards>

<adhd_friendly_principles>
- **Low Friction**: Never block capture to Inbox.
- **Batch Processing**: Organize in weekly sessions rather than constant daily tweaks.
- **Links Over Hierarchy**: Trust search and backlinks rather than deep nesting.
- **Safety Net**: Commit frequently to Git to allow experimentation and easy reverts.
</adhd_friendly_principles>

<git_workflow>
Always commit organizational changes with descriptive messages:
```bash
git add -A
git commit -m "Deduplicate: Merged X duplicate files in Y area"
git push
```
</git_workflow>

<resources>
<reference_index>
- Refer to legacy `SKILL.md` for deduplication strategies, detailed PARA rules, and committee proposal formats.
</reference_index>
</resources>
</skill>
