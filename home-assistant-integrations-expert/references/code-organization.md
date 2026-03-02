## Code Organization

### Core Locations
- Shared constants: `homeassistant/const.py` (use these instead of hardcoding)
- Integration structure:
  - `homeassistant/components/{domain}/const.py` - Constants
  - `homeassistant/components/{domain}/models.py` - Data models
  - `homeassistant/components/{domain}/coordinator.py` - Update coordinator
  - `homeassistant/components/{domain}/config_flow.py` - Configuration flow
  - `homeassistant/components/{domain}/{platform}.py` - Platform implementations

### Common Modules
- **coordinator.py**: Centralize data fetching logic
  ```python
  class MyCoordinator(DataUpdateCoordinator[MyData]):
      def __init__(self, hass: HomeAssistant, client: MyClient, config_entry: ConfigEntry) -> None:
          super().__init__(
              hass,
              logger=LOGGER,
              name=DOMAIN,
              update_interval=timedelta(minutes=1),
              config_entry=config_entry,  # ✅ Pass config_entry - it's accepted and recommended
          )
  ```
- **entity.py**: Base entity definitions to reduce duplication
  ```python
  class MyEntity(CoordinatorEntity[MyCoordinator]):
      _attr_has_entity_name = True
  ```

### Runtime Data Storage
- **Use ConfigEntry.runtime_data**: Store non-persistent runtime data
  ```python
  type MyIntegrationConfigEntry = ConfigEntry[MyClient]

  async def async_setup_entry(hass: HomeAssistant, entry: MyIntegrationConfigEntry) -> bool:
      client = MyClient(entry.data[CONF_HOST])
      entry.runtime_data = client
  ```

### Manifest Requirements
- **Required Fields**: `domain`, `name`, `codeowners`, `integration_type`, `documentation`, `requirements`
- **Integration Types**: `device`, `hub`, `service`, `system`, `helper`
- **IoT Class**: Always specify connectivity method (e.g., `cloud_polling`, `local_polling`, `local_push`)
- **Discovery Methods**: Add when applicable: `zeroconf`, `dhcp`, `bluetooth`, `ssdp`, `usb`
- **Dependencies**: Include platform dependencies (e.g., `application_credentials`, `bluetooth_adapters`)

### Config Flow Patterns
- **Version Control**: Always set `VERSION = 1` and `MINOR_VERSION = 1`
- **Unique ID Management**:
  ```python
  await self.async_set_unique_id(device_unique_id)
  self._abort_if_unique_id_configured()
  ```
- **Error Handling**: Define errors in `strings.json` under `config.error`
- **Step Methods**: Use standard naming (`async_step_user`, `async_step_discovery`, etc.)

### Integration Ownership
- **manifest.json**: Add GitHub usernames to `codeowners`:
  ```json
  {
    "domain": "my_integration",
    "name": "My Integration",
    "codeowners": ["@me"]
  }
  ```

### Async Dependencies (Platinum)
- **Requirement**: All dependencies must use asyncio
- Ensures efficient task handling without thread context switching

### WebSession Injection (Platinum)
- **Pass WebSession**: Support passing web sessions to dependencies
  ```python
  async def async_setup_entry(hass: HomeAssistant, entry: MyConfigEntry) -> bool:
      """Set up integration from config entry."""
      client = MyClient(entry.data[CONF_HOST], async_get_clientsession(hass))
  ```
- For cookies: Use `async_create_clientsession` (aiohttp) or `create_async_httpx_client` (httpx)

### Data Update Coordinator
- **Standard Pattern**: Use for efficient data management
  ```python
  class MyCoordinator(DataUpdateCoordinator):
      def __init__(self, hass: HomeAssistant, client: MyClient, config_entry: ConfigEntry) -> None:
          super().__init__(
              hass,
              logger=LOGGER,
              name=DOMAIN,
              update_interval=timedelta(minutes=5),
              config_entry=config_entry,  # ✅ Pass config_entry - it's accepted and recommended
          )
          self.client = client

      async def _async_update_data(self):
          try:
              return await self.client.fetch_data()
          except ApiError as err:
              raise UpdateFailed(f"API communication error: {err}")
  ```
- **Error Types**: Use `UpdateFailed` for API errors, `ConfigEntryAuthFailed` for auth issues
- **Config Entry**: Always pass `config_entry` parameter to coordinator - it's accepted and recommended

