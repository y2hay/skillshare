## Testing Requirements

- **Location**: `tests/components/{domain}/`
- **Coverage Requirement**: Above 95% test coverage for all modules
- **Best Practices**:
  - Use pytest fixtures from `tests.common`
  - Mock all external dependencies
  - Use snapshots for complex data structures
  - Follow existing test patterns

### Config Flow Testing
- **100% Coverage Required**: All config flow paths must be tested
- **Test Scenarios**:
  - All flow initiation methods (user, discovery, import)
  - Successful configuration paths
  - Error recovery scenarios
  - Prevention of duplicate entries
  - Flow completion after errors

### Testing
- **Integration-specific tests** (recommended):
  ```bash
  pytest ./tests/components/<integration_domain> \
    --cov=homeassistant.components.<integration_domain> \
    --cov-report term-missing \
    --durations-min=1 \
    --durations=0 \
    --numprocesses=auto
  ```

### Testing Best Practices
- **Never access `hass.data` directly** - Use fixtures and proper integration setup instead
- **Use snapshot testing** - For verifying entity states and attributes
- **Test through integration setup** - Don't test entities in isolation
- **Mock external APIs** - Use fixtures with realistic JSON data
- **Verify registries** - Ensure entities are properly registered with devices

### Config Flow Testing Template
```python
async def test_user_flow_success(hass, mock_api):
    """Test successful user flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"

    # Test form submission
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
    """Overridden fixture to specify platforms to test."""
    return [Platform.SENSOR]  # Or another specific platform as needed.

@pytest.mark.usefixtures("entity_registry_enabled_by_default", "init_integration")
async def test_entities(
    hass: HomeAssistant,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    device_registry: dr.DeviceRegistry,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test the sensor entities."""
    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)

    # Ensure entities are correctly assigned to device
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

### Mock Patterns
```python
# Modern integration fixture setup
@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Return the default mocked config entry."""
    return MockConfigEntry(
        title="My Integration",
        domain=DOMAIN,
        data={CONF_HOST: "127.0.0.1", CONF_API_KEY: "test_key"},
        unique_id="device_unique_id",
    )

@pytest.fixture
def mock_device_api() -> Generator[MagicMock]:
    """Return a mocked device API."""
    with patch("homeassistant.components.my_integration.MyDeviceAPI", autospec=True) as api_mock:
        api = api_mock.return_value
        api.get_data.return_value = MyDeviceData.from_json(
            load_fixture("device_data.json", DOMAIN)
        )
        yield api

@pytest.fixture
def platforms() -> list[Platform]:
    """Fixture to specify platforms to test."""
    return PLATFORMS

@pytest.fixture
async def init_integration(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_device_api: MagicMock,
    platforms: list[Platform],
) -> MockConfigEntry:
    """Set up the integration for testing."""
    mock_config_entry.add_to_hass(hass)

    with patch("homeassistant.components.my_integration.PLATFORMS", platforms):
        await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

    return mock_config_entry
```

