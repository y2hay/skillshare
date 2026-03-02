---
name: home-assistant-integrations-expert
description: Expert guidance for developing Home Assistant integrations following the latest architectural patterns, quality scale requirements, and testing standards. Supports everything from core organization to entity development and platinum-level quality standards.
---

<skill>
<objective>
Provide expert-level support for developing, optimizing, and testing Home Assistant integrations, ensuring compliance with architectural standards and quality scale requirements.
</objective>

<quick_start>
Follow the Standard Integration Structure for new projects. Use the `DataUpdateCoordinator` for polling and ensure all entities have `unique_id`s. Consult `references/testing-requirements.md` for mandatory test coverage.
</quick_start>

<success_criteria>
- Integrations follow the standard file structure and manifest requirements
- Config flows are implemented with full support for re-authentication and discovery
- Entities use descriptions, handle lifecycles correctly, and provide availability status
- Test coverage includes config flows, entity states, and mock service interactions
- Code adheres to the Home Assistant Quality Scale (striving for Gold/Platinum)
</success_criteria>

<core_principles>
- **Async-First**: All I/O must be non-blocking. Use `hass.async_add_executor_job` for blocking calls.
- **Single Source of Truth**: Use `DataUpdateCoordinator` to manage shared state.
- **Portable Config**: Use Config Entries exclusively (no `configuration.yaml` setup).
- **Quality Scale**: Follow the `quality_scale.yaml` rules for your target level.
</core_principles>

<resources>
<reference_index>
- **references/templates-and-quality.md**: Standard integration structure and Quality Scale levels
- **references/code-organization.md**: Module locations, manifest requirements, and data storage
- **references/integration-guidelines.md**: Config flows, discovery, and service registration
- **references/entity-development.md**: Unique IDs, naming, state handling, and availability
- **references/device-management.md**: Device registry, categories, translations, and icons
- **references/testing-requirements.md**: Mock patterns and testing templates for flows and entities
- **references/debugging.md**: Debug logging, validation commands, and common issues
</reference_index>

<file_locations>
- **Core**: `homeassistant/components/INTEGRATION/`
- **Custom**: `config/custom_components/INTEGRATION/`
</file_locations>
</resources>
</skill>
