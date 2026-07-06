---
name: home-assistant-integrations-expert
description: >
  Expert guidance for developing Home Assistant integrations — config flows,
  entities, testing, quality scale, and architectural patterns. Triggered when
  creating or reviewing integrations, config flows, or aiming for Silver/Gold/Platinum
  quality scale ratings.
version: 1
triggers: ["HA integration", "create integration", "config flow", "Quality Scale", "Silver", "Gold", "Platinum"]
allowed-tools: [bash, python, editor, terminal]
---

<skill>
<objective>
Provide expert-level support for developing, optimizing, and testing Home Assistant integrations, ensuring compliance with architectural standards and quality scale requirements.
</objective>

<quick_start>
Follow the Standard Integration Structure for new projects. Use the `DataUpdateCoordinator` for polling and ensure all entities have `unique_id`s. Aim for 95%+ test coverage covering all config flow paths.
</quick_start>

<success_criteria>
- Integrations follow the standard file structure and manifest requirements
- Config flows are implemented with full support for re-authentication and discovery
- Entities use descriptions, handle lifecycles correctly, and provide availability status
- Test coverage includes config flows, entity states, and mock service interactions (95%+)
- Code adheres to the Home Assistant Quality Scale (striving for Gold/Platinum)
</success_criteria>

<core_principles>
- **Async-First**: All I/O must be non-blocking. Use `hass.async_add_executor_job` for blocking calls.
- **Single Source of Truth**: Use `DataUpdateCoordinator` to manage shared state.
- **Portable Config**: Use Config Entries exclusively (no `configuration.yaml` setup).
- **Quality Scale**: Follow the `quality_scale.yaml` rules for your target level.
- **Config Flow Required**: Set `"config_flow": true` in manifest.json — all integrations must support UI setup.
</core_principles>

## Integration Guidelines (Condensed)

### Configuration Flow

- **UI Setup Required**: All integrations must support configuration via UI
- **Manifest**: Set `"config_flow": true` in `manifest.json`
- **Data Storage**:
  - Connection-critical config: Store in `ConfigEntry.data`
  - Non-critical settings: Store in `ConfigEntry.options`
- **Validation**: Always validate user input before creating entries
- **Config Entry Naming**:
  - ❌ Do NOT allow users to set config entry names in config flows
  - Names are automatically generated or can be customized later in UI
  - ✅ Exception: Helper integrations MAY allow custom names in config flow
- **Connection Testing**: Test device/service connection during config flow:
  ```python
  try:
      await client.get_data()
  except MyException:
      errors["base"] = "cannot_connect"
  ```
- **Duplicate Prevention**:
  ```python
  await self.async_set_unique_id(identifier)
  self._abort_if_unique_id_configured()
  ```

### Reauthentication & Reconfiguration

- **Required Method**: Implement `async_step_reauth` in config flow
- **Validation**: Verify account matches existing unique ID:
  ```python
  await self.async_set_unique_id(user_id)
  self._abort_if_unique_id_mismatch(reason="wrong_account")
  return self.async_update_reload_and_abort(
      self._get_reauth_entry(),
      data_updates={CONF_API_TOKEN: user_input[CONF_API_TOKEN]}
  )
  ```
- **Reconfiguration**: Add `async_step_reconfigure` for config updates without removing device

### Device Discovery

- **Manifest Configuration**: Add discovery method (zeroconf, dhcp, etc.)
  ```json
  { "zeroconf": ["_mydevice._tcp.local."] }
  ```
- **Discovery Handler**: Implement `async_step_zeroconf` (or ssdp/bluetooth)
- **Network Updates**: Use discovery to update dynamic IP addresses

### Setup Validation & Unloading

- **Exception Handling**:
  - `ConfigEntryNotReady`: Device offline or temporary failure
  - `ConfigEntryAuthFailed`: Authentication issues
  - `ConfigEntryError`: Unresolvable setup problems
- **Unloading**: Implement `async_unload_entry` — register callbacks with `entry.async_on_unload`

### Polling

- Use `DataUpdateCoordinator` pattern
- **Polling intervals are NOT user-configurable** — set programmatically
- **Minimum Intervals**: Local network → 5s, Cloud services → 60s
- **Parallel Updates**: `PARALLEL_UPDATES = 1` (serialize) or `0` (unlimited for coordinator-based)

### Service Actions

- Register in `async_setup`, NOT in `async_setup_entry`
- Validate config entry existence and loaded state
- Create `services.yaml` with descriptions and field definitions

## Testing Requirements (Condensed)

### Coverage

- **Location**: `tests/components/{domain}/`
- **Coverage Requirement**: Above 95% for all modules
- **Config Flow Coverage**: 100% — all paths (user, discovery, import, error recovery, duplicate prevention)

### Best Practices

- Use pytest fixtures from `tests.common`
- Mock all external dependencies
- Use snapshots for complex data structures
- **Never access `hass.data` directly** — use fixtures and proper integration setup
- **Test through integration setup** — don't test entities in isolation
- Verify registries — ensure entities are properly registered with devices

### Config Flow Testing Template

```python
async def test_user_flow_success(hass, mock_api):
    """Test successful user flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=TEST_USER_INPUT
    )
    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "My Device"
    assert result["data"] == TEST_USER_INPUT

async def test_flow_connection_error(hass, mock_api_error):
    """Test connection error handling."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=TEST_USER_INPUT
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}
```

### Entity Testing Patterns

```python
@pytest.fixture
def platforms() -> list[Platform]:
    return [Platform.SENSOR]

@pytest.mark.usefixtures("entity_registry_enabled_by_default", "init_integration")
async def test_entities(
    hass: HomeAssistant,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    device_registry: dr.DeviceRegistry,
    mock_config_entry: MockConfigEntry,
) -> None:
    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)

    device_entry = device_registry.async_get_device(
        identifiers={(DOMAIN, "device_unique_id")}
    )
    assert device_entry
    entity_entries = er.async_entries_for_config_entry(
        entity_registry, mock_config_entry.entry_id
    )
    for entity_entry in entity_entries:
        assert entity_entry.device_id == device_entry.id
```

### Mock Fixture Pattern

```python
@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    return MockConfigEntry(
        title="My Integration",
        domain=DOMAIN,
        data={CONF_HOST: "127.0.0.1", CONF_API_KEY: "test_key"},
        unique_id="device_unique_id",
    )

@pytest.fixture
def mock_device_api() -> Generator[MagicMock]:
    with patch("homeassistant.components.my_integration.MyDeviceAPI", autospec=True) as api_mock:
        api = api_mock.return_value
        api.get_data.return_value = MyDeviceData.from_json(
            load_fixture("device_data.json", DOMAIN)
        )
        yield api

@pytest.fixture
async def init_integration(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_device_api: MagicMock,
    platforms: list[Platform],
) -> MockConfigEntry:
    mock_config_entry.add_to_hass(hass)
    with patch("homeassistant.components.my_integration.PLATFORMS", platforms):
        await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()
    return mock_config_entry
```

## Reference Files

For full details, consult the reference files in this skill directory:

- **references/templates-and-quality.md**: Standard integration structure and Quality Scale levels
- **references/code-organization.md**: Module locations, manifest requirements, and data storage
- **references/integration-guidelines.md**: Full config flows, discovery, and service registration
- **references/entity-development.md**: Unique IDs, naming, state handling, and availability
- **references/device-management.md**: Device registry, categories, translations, and icons
- **references/testing-requirements.md**: Full mock patterns and testing templates
- **references/debugging.md**: Debug logging, validation commands, and common issues
- **references/platform-repairs.md**: Repairs/flows platform patterns
- **references/platform-diagnostics.md**: Diagnostics platform patterns

</skill>
