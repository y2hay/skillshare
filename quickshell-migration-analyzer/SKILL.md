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
