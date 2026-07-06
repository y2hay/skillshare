---

name: Skill Development
description: |
  Use when creating or improving agent skills; triggers include "create a skill", "write a new skill", "improve skill description", "skill structure", and "progressive disclosure".
version: 0.1.0

---

<skill>
<objective>
Provide comprehensive guidance for creating, organizing, and optimizing skills for Claude Code plugins, focusing on progressive disclosure and effective AI-to-AI communication.
</objective>

<quick_start>
Follow the 6-step Skill Creation Process. Write instructions in the imperative/infinitive form. Use third-person trigger phrases in the description. Extract detailed content to `references/` to keep `SKILL.md` under 2,000 words.
</quick_start>

<success_criteria>
- Skills load reliably based on specific trigger phrases in the description
- `SKILL.md` is focused and lean (1,500-2,000 words)
- Detailed content is correctly moved to `references/` and loaded as needed
- Instructions use imperative form ("Do X") rather than second person ("You should do X")
- Utility scripts are executable and documented
</success_criteria>

<anatomy_of_a_skill>
```
skill-name/
├── SKILL.md (required) - Metadata and core instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code (Python/Bash/etc.)
    ├── references/ - Detailed documentation loaded into context as needed
    └── assets/     - Output files (templates, images, fonts)
```
</anatomy_of_a_skill>

<progressive_disclosure_levels>
1. **Metadata (name + description)**: Always in context (~100 words).
2. **SKILL.md body**: Loaded when skill triggers (&lt;5k words).
3. **Bundled resources**: Loaded/executed as needed by Claude (unlimited).
</progressive_disclosure_levels>

<plugin_considerations>
- **Location**: `my-plugin/skills/my-skill/SKILL.md`
- **Auto-Discovery**: Claude Code automatically scans the `skills/` directory.
- **Distribution**: Skills are part of the plugin package; no separate ZIP needed.
- **Testing**: Test locally using `cc --plugin-dir /path/to/plugin`.
</plugin_considerations>

<resources>
<reference_index>
- **references/creation-process.md**: Step-by-step guide from planning to iteration
- **references/progressive-disclosure.md**: Designing for context efficiency
- **references/writing-style.md**: Imperative form and objective language requirements
- **references/common-mistakes.md**: Avoiding weak triggers and context bloat
- **references/skill-creator-original.md**: Full original methodology
</reference_index>

<best_practices_summary>
- ✅ Use third-person in description
- ✅ Include specific trigger phrases
- ✅ Keep SKILL.md lean (1,500-2,000 words)
- ✅ Write in imperative form
- ✅ Reference supporting files clearly
</best_practices_summary>
</resources>
</skill>
