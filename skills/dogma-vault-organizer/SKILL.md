---

name: dogma-vault-organizer
description: |
  Use when organizing the ~/dogma vault or knowledge base; triggers include "organize dogma vault", "deduplicate notes", "PARA cleanup", "clean my knowledge base", and "sort vault files". Maintains vault structure, deduplication, and PARA compliance.
version: 1
triggers: ["organize vault", "deduplicate dogma", "process inbox", "PARA cleanup"]

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

<deduplication_rules>
When scanning for duplicates:
1. **Exact match**: Same filename + same content → keep newest, delete rest.
2. **Content match**: Different names but identical body → merge into single canonical file, add redirect/alias.
3. **Fuzzy match**: Similar content (80%+ overlap) → consolidate key insights into one file, link to source.
4. **Cross-PARA duplicates**: Same concept found in multiple PARA folders → move to most appropriate single location, cross-link from others.
5. **Draft consolidation**: Multiple drafts of same idea → merge into final version, archive drafts.
</deduplication_rules>

<weekly_organization_process>
1. **Process Inbox** (`00_Inbox`)
   ```bash
   ls ~/dogma/00_Inbox/ | wc -l        # count inbox items
   ```
   - Read each file, classify into Projects/Areas/Resources/Archive
   - Files staying in Inbox >7 days get priority review
   - Target: <20 items remaining

2. **Scan for Duplicates**
   ```bash
   fdupes -r ~/dogma/                   # find exact duplicates
   ```
   - Review and merge or delete duplicates per deduplication rules
   - Commit after each batch: `git commit -m "Deduplicate: Merged $N files in $AREA"`

3. **Review Projects** (`01_Projects`)
   - Check each project folder: still active? → keep. Completed? → archive.
   - Update project status in filenames or metadata

4. **Fix Broken Links**
   ```bash
   rg -l '\[\[.*?\]\]' ~/dogma/        # find all wiki links, verify targets exist
   ```
   - Repair or remove broken `[[WikiLinks]]`

5. **Git Commit**
   ```bash
   git -C ~/dogma add -A && git -C ~/dogma commit -m "Weekly org: processed inbox, dedup, archived projects"
   ```
</weekly_organization_process>
</skill>
