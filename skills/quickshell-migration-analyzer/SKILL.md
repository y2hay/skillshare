---
name: quickshell-migration-analyzer
description: "Expert QuickShell/QML analyzer for identifying reusable modules and components that can be migrated from DMS to Caelestia. Evaluates architectural compatibility, dependencies, and migration complexity."
globs:
  - "**/*.qml"
  - "**/CLAUDE.md"
  - "**/README.md"
---

<skill>
<objective>
Expertly identify and evaluate QML modules, components, and patterns for migration from DankMaterialShell (DMS) to Caelestia QuickShell environments, providing tiered recommendations based on complexity and value.
</objective>

<quick_start>
Locate DMS and Caelestia directories. Catalog DMS components (Services, Modules, Widgets). Analyze dependencies and score each candidate using the Complexity Matrix. Generate a tiered migration report.
</quick_start>

<success_criteria>
- Comprehensive inventory of DMS components is established with categorized dependencies
- Components are accurately scored for Standalone capability, Adaptation Effort, and Value
- Migration tiers (Quick Wins, Medium Effort, Heavy Lift) are clearly defined
- Final report provides actionable migration steps, including import path updates and theme adaptation
</success_criteria>

<core_analysis_methodology>
<phase_1_discovery>
1. **Locate Projects**: Find DMS and Caelestia installations using `find`.
2. **Map Structures**: Catalog entry points and directory layouts.
3. **Extract Context**: Read `CLAUDE.md` and `README.md` for architectural patterns.
</phase_1_discovery>

<phase_2_inventory>
1. **Catalog Components**: Map `Services/`, `Modules/`, `Widgets/`, `Common/`, and `Modals/`.
2. **Analyze Dependencies**: Check for external Qt imports, framework dependencies, and internal service references.
3. **Evaluate Complexity**:
   - **Standalone Score (1-5)**: Degree of isolation.
   - **Adaptation Effort (1-5)**: Effort to refactor for Caelestia.
   - **Value Proposition (1-5)**: Importance of functionality.
</phase_2_inventory>

<phase_3_compatibility>
1. **Map Caelestia Architecture**: Identify existing patterns and service structures.
2. **Identify Gaps/Overlaps**: Find unique DMS components or superior implementations.
</phase_3_compatibility>

<phase_4_recommendations>
1. **Categorize into Tiers**:
   - **Tier 1 (Quick Wins)**: High standalone/value, low effort.
   - **Tier 2 (Medium Effort)**: Moderate complexity, high value.
   - **Tier 3 (Heavy Lift)**: Low isolation, requires major refactoring.
2. **Document Findings**: Generate structured reports with component location, scores, and specific migration notes.
</phase_4_recommendations>
</core_analysis_methodology>

<evaluation_framework>
<architectural_patterns>
- **DMS-Specific**: Singleton services (`id: root`), Material Design 3 styling, SettingsData/SessionData.
- **Transferable**: Pure QML/QtQuick, stateless utility functions, modular widgets.
</architectural_patterns>

<warning_signs>
- Deep coupling to DMS singletons
- Hardcoded paths
- Dependencies on missing compositor-specific APIs
</warning_signs>

<good_candidates>
- Standalone UI widgets
- Pure visual components/animations
- Modular helper scripts (JS)
</good_candidates>
</evaluation_framework>

<output_guidelines>
Reports must include:
1. **Executive Summary**: Counts by tier.
2. **Tiered Details**: For each component, provide location, scores, description, dependencies, and steps.
3. **Migration Sequence**: Recommended order of implementation.
</output_guidelines>

<resources>
<reference_index>
- Refer to `SKILL.md` (legacy) for full workflow and reporting templates.
</reference_index>
</resources>
</skill>


---
# Additional Documentation from Legacy Version


## Tier 2: Medium Effort
[Similar format for Tier 2 components]

## Tier 3: Heavy Lift
[Similar format for Tier 3 components]

## Not Recommended for Migration
[List with brief rationale]

## Architecture Compatibility Notes
- Theme system differences: [details]
- Service layer considerations: [details]
- Integration points needed: [details]

## Recommended Migration Sequence
1. Start with Tier 1 widgets (low risk, immediate value)
2. Evaluate Tier 2 after establishing patterns
3. Consider Tier 3 only if critical functionality missing
```

</output_guidelines>

## Best Practices

<best_practices>

### Analysis Approach
- **Breadth-first:** Catalog all components before deep analysis
- **Dependency mapping:** Use Grep to find all import/usage patterns
- **Comparative analysis:** Always check if Caelestia has equivalent
- **Value-driven:** Prioritize by ROI (value vs. effort)

### Tool Usage
- **Glob:** Efficiently find all QML files by category
- **Read:** Examine component implementation details
- **Grep:** Map dependencies and usage patterns
- **Bash:** Run targeted searches for architectural patterns

### Communication Style
- **Structured:** Use clear categorization and scoring
- **Actionable:** Provide concrete migration steps
- **Honest:** Flag real challenges and risks
- **Prioritized:** Order by migration feasibility

</best_practices>

## Example Interaction

<example_usage>

**User:** "Analyze DMS for components we can migrate to Caelestia"

**You should:**
1. Locate both DMS and Caelestia installations
2. Read architectural docs (CLAUDE.md, README.md)
3. Catalog DMS components by directory
4. For each promising component:
   - Analyze dependencies
   - Score on complexity matrix
   - Assess Caelestia compatibility
5. Generate tiered migration report with specific recommendations

**User:** "Focus on the Widgets directory - what can we take?"

**You should:**
1. Glob all files in DMS Widgets/
2. Read each widget implementation
3. Identify dependencies (imports, services, theme)
4. Score each widget on complexity matrix
5. Provide ranked list with migration instructions for top candidates

</example_usage>

---

**Remember:** Your goal is to provide **actionable intelligence** that enables confident migration decisions. Balance thoroughness with pragmatism - not everything should be migrated, and that's okay. Focus on high-value, low-effort wins first.
