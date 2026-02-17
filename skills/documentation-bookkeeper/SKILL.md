---
name: documentation-bookkeeper
description: Audits all .md documentation files to ensure information is organized in appropriate locations, suggests restructuring, and can move content 1:1 without data loss. Run 4 times daily or when documentation grows disorganized.
---

# Documentation Bookkeeper

## Purpose

This skill reviews all markdown documentation files in the knowledge base and ensures information is properly organized. It identifies misplaced content, suggests better locations, and can reorganize documentation while preserving all information 1:1 (never removing anything).

## When to Use This Skill

**Automatic (Proactive):**
- After any session that creates/updates multiple .md files
- When changelog entries could belong in other documentation
- When architecture details are scattered across multiple files
- When new categories of information emerge that need dedicated files

**Manual (On Request):**
- User says "organize documentation" or "audit the docs"
- User says "run bookkeeper" or similar
- When documentation feels cluttered or hard to navigate
- **Schedule: 4 times per day** during active development

## Documentation Structure Philosophy

### Core Files (Must Exist)

1. **CLAUDE.md** - System architecture, runbooks, decisions index
   - Network topology
   - Infrastructure layout (Proxmox, LXCs, Docker)
   - Service dependencies and DNS architecture
   - Runbooks for recurring procedures
   - Decision log (index only - details in changelog)
   - Session start protocol and workflow requirements

2. **CLAUDE_CHANGELOG.md** - Historical record of changes
   - Chronological log of all changes and decisions
   - Implementation details with rationale
   - Full context for why decisions were made
   - Troubleshooting sessions and resolutions
   - Links to external sources
   - **Should NOT contain:** General how-to guides, permanent reference material

3. **CREDENTIALS.md** - Service credentials and API keys
   - Login credentials for all services
   - API tokens and keys
   - Password references
   - Security notes

### Potential New Files (Create As Needed)

The bookkeeper should suggest creating new files when content naturally clusters:

- **NETWORKING.md** - Deep dive into network configuration
- **DNS_SETUP.md** - Complete DNS architecture reference (Pi-hole, Unbound, DoH/DoT)
- **PRIVACY_SECURITY.md** - VPN decisions, encryption, security practices
- **MEDIA_STACK.md** - Arr stack configuration, torrent/Usenet setup
- **HOMELAB_DECISIONS.md** - Permanent reference for architectural decisions
- **TROUBLESHOOTING.md** - Common issues and solutions (separate from runbooks)
- **[SERVICE]_GUIDE.md** - Dedicated guides for complex services

## Audit Process

### Step 1: Scan All Documentation

Read all .md files in:
- `/home/xcx/CLAUDE.md`
- `/home/xcx/.claude/CLAUDE.md`
- `/home/xcx/CLAUDE_CHANGELOG.md`
- `/home/xcx/CREDENTIALS.md`
- `/home/xcx/*.md` (any other markdown files)
- `/home/xcx/claude-knowledge/*.md` (NFS-mounted centralized docs)

### Step 2: Identify Organization Issues

Look for these red flags:

1. **Changelog Bloat:**
   - General reference material in changelog (should be in CLAUDE.md or dedicated guide)
   - Decision analysis that's reference material not historical record
   - How-to guides in changelog (should be in dedicated guides)
   - VPN/privacy analysis (should be in PRIVACY_SECURITY.md)

2. **CLAUDE.md Overload:**
   - Excessive detail drowning out architecture overview
   - Content that could be in dedicated guides
   - Temporary information that should be in changelog only

3. **Missing Structure:**
   - Related information scattered across multiple files
   - No clear home for emerging categories
   - Complex topics mixed with simple references

4. **Duplication:**
   - Same information in multiple locations
   - Outdated copies of information
   - Conflicting information between files

### Step 3: Generate Reorganization Proposal

Create a proposal that:

1. **Lists Issues Found:**
   ```
   - VPN necessity analysis in CLAUDE_CHANGELOG.md (628 lines)
     Problem: This is reference material, not historical change
     Suggestion: Move to new PRIVACY_SECURITY.md

   - DNS architecture details scattered between CLAUDE.md and changelog
     Problem: Hard to find complete picture
     Suggestion: Create DNS_SETUP.md with full reference
   ```

2. **Proposes New Files:**
   ```
   Suggested new file: PRIVACY_SECURITY.md
   Purpose: Centralized reference for privacy/security decisions
   Content to include:
     - VPN necessity analysis (from changelog)
     - Encrypted DNS explanation (from changelog)
     - Unbound setup rationale
     - Future: Firewall rules, access controls, etc.
   ```

3. **Shows Move Plan:**
   ```
   Move #1: CLAUDE_CHANGELOG.md lines 190-233 → PRIVACY_SECURITY.md
     - VPN Necessity Analysis section
     - Keep 1-line reference in changelog: "See PRIVACY_SECURITY.md for VPN analysis"

   Move #2: CLAUDE_CHANGELOG.md lines 151-189 → DNS_SETUP.md
     - DNS over HTTPS/TLS investigation
     - Keep historical note: "Investigated DoH/DoT - see DNS_SETUP.md for details"
   ```

### Step 4: Request Approval

Present the proposal to the user:

```
Documentation Audit Complete
============================

Found 3 organizational issues:

1. PRIVACY/SECURITY CONTENT IN CHANGELOG
   - 45 lines of VPN analysis (reference material)
   - Belongs in: PRIVACY_SECURITY.md (new file)

2. DNS ARCHITECTURE SCATTERED
   - Details in 3 different locations
   - Belongs in: DNS_SETUP.md (new file)

3. DUPLICATE NETWORK TOPOLOGY
   - In both CLAUDE.md files
   - Action: Consolidate to ~/.claude/CLAUDE.md only

Proposed changes:
- Create PRIVACY_SECURITY.md (move 45 lines from changelog)
- Create DNS_SETUP.md (move 89 lines from changelog + 30 from CLAUDE.md)
- Remove duplicate from /home/xcx/CLAUDE.md

Approve reorganization? (yes/no)
If approved, all moves will be 1:1 - no information will be lost.
```

### Step 5: Execute Approved Moves

When user approves:

1. **Create new files** with proper headers
2. **Copy content 1:1** (never summarize or remove)
3. **Replace original with reference link:**
   - Changelog: Brief note + "See [FILE].md for details"
   - Other files: Link to new location
4. **Verify nothing lost** - character count before/after
5. **Update in single atomic operation** when possible

## Critical Rules

### NEVER Remove Information

- ❌ Don't summarize when moving
- ❌ Don't condense or paraphrase
- ❌ Don't delete "redundant" information
- ✅ Copy exact text 1:1
- ✅ Keep all formatting, links, code blocks
- ✅ Verify character counts match

### Always Get Approval

- ❌ Don't reorganize without user consent
- ❌ Don't create new files automatically
- ✅ Present proposal first
- ✅ Wait for explicit approval
- ✅ Allow user to modify plan

### Preserve History

- Keep historical changelog entries even when moving content
- Replace with reference: "Moved to [FILE].md - see there for details"
- Never delete changelog entries
- Maintain chronological order

### Link Everything

When moving content:
- Original location gets link to new location
- New file references original changelog entry date
- Cross-reference related information
- Maintain bidirectional links

## Example Reorganization

### Before:
```
CLAUDE_CHANGELOG.md (450 lines)
  - VPN analysis (45 lines)
  - DNS investigation (89 lines)
  - Pi-hole IPv6 fix (120 lines)
  - Quickshell rebuild (196 lines)

CLAUDE.md (200 lines)
  - Network topology (30 lines)
  - DNS architecture (35 lines)
  - Everything else (135 lines)
```

### After:
```
CLAUDE_CHANGELOG.md (300 lines)
  - Brief entry: "VPN analysis - see PRIVACY_SECURITY.md"
  - Brief entry: "DNS investigation - see DNS_SETUP.md"
  - Pi-hole IPv6 fix (120 lines) ← Historical, stays
  - Quickshell rebuild (196 lines) ← Historical, stays

CLAUDE.md (150 lines)
  - Network topology (30 lines)
  - DNS architecture (20 lines, overview only)
  - Link: "See DNS_SETUP.md for complete DNS documentation"
  - Everything else (100 lines)

DNS_SETUP.md (NEW - 154 lines)
  - Complete DNS architecture reference
  - Pi-hole configuration
  - Unbound setup
  - DoH/DoT investigation results
  - IPv6 DNS configuration
  - Moved from: changelog + CLAUDE.md

PRIVACY_SECURITY.md (NEW - 45 lines)
  - VPN necessity analysis
  - Encrypted DNS explanation
  - Moved from: changelog
```

## Output Format

Generate a report like this:

```markdown
# Documentation Audit Report
**Date:** 2025-12-02
**Files Scanned:** 4
**Issues Found:** 3
**Files to Create:** 2

## Issues

### 1. Reference Material in Changelog
**Severity:** Medium
**Location:** CLAUDE_CHANGELOG.md lines 190-233
**Issue:** VPN analysis is permanent reference material, not historical change log
**Recommendation:** Move to PRIVACY_SECURITY.md (new file)
**Impact:** Makes changelog cleaner, easier to find VPN info in future

### 2. DNS Documentation Scattered
**Severity:** Medium
**Locations:**
  - CLAUDE_CHANGELOG.md lines 151-189
  - CLAUDE.md lines 85-94
**Issue:** No single source of truth for DNS architecture
**Recommendation:** Create DNS_SETUP.md with all DNS documentation
**Impact:** Single comprehensive DNS reference

## Proposed Changes

### Create PRIVACY_SECURITY.md
**Content:**
- VPN necessity analysis (45 lines from changelog)
- Future: Firewall rules, access controls

**Changelog Edit:**
Replace lines 190-233 with:
"See PRIVACY_SECURITY.md for VPN analysis and privacy/security decisions"

### Create DNS_SETUP.md
**Content:**
- Full DNS architecture (from CLAUDE.md)
- Pi-hole setup details (from changelog)
- Unbound configuration (from changelog)
- DoH/DoT investigation (from changelog)

**CLAUDE.md Edit:**
Replace detailed DNS section with:
"See DNS_SETUP.md for complete DNS configuration and architecture"

**Changelog Edits:**
Multiple sections - replace with references to DNS_SETUP.md

## Approval Required

Type 'yes' to proceed with reorganization.
All moves will be 1:1 copies - no information will be lost.
```

## Anti-Patterns to Avoid

❌ **Don't move everything out of changelog**
- Historical entries belong there
- Troubleshooting sessions are historical
- Implementation logs are historical

❌ **Don't create too many files**
- Only create new files when content naturally clusters
- Aim for 5-10 well-organized files, not 50 tiny ones
- Related content should stay together

❌ **Don't break links**
- Update all cross-references
- Maintain bidirectional links
- Test links after reorganization

❌ **Don't lose context**
- Keep enough context in changelog entries
- Don't remove the "why" when moving the "what"
- Preserve decision rationale

## Success Criteria

✅ Each file has clear, singular purpose
✅ Information is easy to find
✅ No duplication (except intentional cross-references)
✅ Changelog is chronological history, not reference manual
✅ CLAUDE.md is architecture overview, not detailed guide
✅ All information preserved 1:1
✅ All cross-references working
✅ User can find information in <30 seconds

## Maintenance Schedule

**Recommended:** Run this skill 4 times per day during active development sessions:
- After morning session
- After midday session
- After afternoon session
- End of day review

**Or run when:**
- Changelog grows beyond 500 lines
- Information is hard to find
- New categories of information emerge
- User requests documentation cleanup
