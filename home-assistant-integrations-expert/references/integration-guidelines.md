## Integration Guidelines

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
- **Duplicate Prevention**: Prevent duplicate configurations:
  ```python
  # Using unique ID
  await self.async_set_unique_id(identifier)
  self._abort_if_unique_id_configured()

  # Using unique data
  self._async_abort_entries_match({CONF_HOST: user_input[CONF_HOST]})
  ```

### Reauthentication Support
- **Required Method**: Implement `async_step_reauth` in config flow
- **Credential Updates**: Allow users to update credentials without re-adding
- **Validation**: Verify account matches existing unique ID:
  ```python
  await self.async_set_unique_id(user_id)
  self._abort_if_unique_id_mismatch(reason="wrong_account")
  return self.async_update_reload_and_abort(
      self._get_reauth_entry(),
      data_updates={CONF_API_TOKEN: user_input[CONF_API_TOKEN]}
  )
  ```

### Reconfiguration Flow
- **Purpose**: Allow configuration updates without removing device
- **Implementation**: Add `async_step_reconfigure` method
- **Validation**: Prevent changing underlying account with `_abort_if_unique_id_mismatch`

### Device Discovery
- **Manifest Configuration**: Add discovery method (zeroconf, dhcp, etc.)
  ```json
  {
    "zeroconf": ["_mydevice._tcp.local."]
  }
  ```
- **Discovery Handler**: Implement appropriate `async_step_*` method:
  ```python
  async def async_step_zeroconf(self, discovery_info):
      """Handle zeroconf discovery."""
      await self.async_set_unique_id(discovery_info.properties["serialno"])
      self._abort_if_unique_id_configured(updates={CONF_HOST: discovery_info.host})
  ```
- **Network Updates**: Use discovery to update dynamic IP addresses

### Network Discovery Implementation
- **Zeroconf/mDNS**: Use async instances
  ```python
  aiozc = await zeroconf.async_get_async_instance(hass)
  ```
- **SSDP Discovery**: Register callbacks with cleanup
  ```python
  entry.async_on_unload(
      ssdp.async_register_callback(
          hass, _async_discovered_device,
          {"st": "urn:schemas-upnp-org:device:ZonePlayer:1"}
      )
  )
  ```

### Bluetooth Integration
- **Manifest Dependencies**: Add `bluetooth_adapters` to dependencies
- **Connectable**: Set `"connectable": true` for connection-required devices
- **Scanner Usage**: Always use shared scanner instance
  ```python
  scanner = bluetooth.async_get_scanner()
  entry.async_on_unload(
      bluetooth.async_register_callback(
          hass, _async_discovered_device,
          {"service_uuid": "example_uuid"},
          bluetooth.BluetoothScanningMode.ACTIVE
      )
  )
  ```
- **Connection Handling**: Never reuse `BleakClient` instances, use 10+ second timeouts

### Setup Validation
- **Test Before Setup**: Verify integration can be set up in `async_setup_entry`
- **Exception Handling**:
  - `ConfigEntryNotReady`: Device offline or temporary failure
  - `ConfigEntryAuthFailed`: Authentication issues
  - `ConfigEntryError`: Unresolvable setup problems

### Config Entry Unloading
- **Required**: Implement `async_unload_entry` for runtime removal/reload
- **Platform Unloading**: Use `hass.config_entries.async_unload_platforms`
- **Cleanup**: Register callbacks with `entry.async_on_unload`:
  ```python
  async def async_unload_entry(hass: HomeAssistant, entry: MyConfigEntry) -> bool:
      """Unload a config entry."""
      if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
          entry.runtime_data.listener()  # Clean up resources
      return unload_ok
  ```

### Service Actions
- **Registration**: Register all service actions in `async_setup`, NOT in `async_setup_entry`
- **Validation**: Check config entry existence and loaded state:
  ```python
  async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
      async def service_action(call: ServiceCall) -> ServiceResponse:
          if not (entry := hass.config_entries.async_get_entry(call.data[ATTR_CONFIG_ENTRY_ID])):
              raise ServiceValidationError("Entry not found")
          if entry.state is not ConfigEntryState.LOADED:
              raise ServiceValidationError("Entry not loaded")
  ```
- **Exception Handling**: Raise appropriate exceptions:
  ```python
  # For invalid input
  if end_date < start_date:
      raise ServiceValidationError("End date must be after start date")

  # For service errors
  try:
      await client.set_schedule(start_date, end_date)
  except MyConnectionError as err:
      raise HomeAssistantError("Could not connect to the schedule") from err
  ```

### Service Registration Patterns
- **Entity Services**: Register on platform setup
  ```python
  platform.async_register_entity_service(
      "my_entity_service",
      {vol.Required("parameter"): cv.string},
      "handle_service_method"
  )
  ```
- **Service Schema**: Always validate input
  ```python
  SERVICE_SCHEMA = vol.Schema({
      vol.Required("entity_id"): cv.entity_ids,
      vol.Required("parameter"): cv.string,
      vol.Optional("timeout", default=30): cv.positive_int,
  })
  ```
- **Services File**: Create `services.yaml` with descriptions and field definitions

### Polling
- Use update coordinator pattern when possible
- **Polling intervals are NOT user-configurable**: Never add scan_interval, update_interval, or polling frequency options to config flows or config entries
- **Integration determines intervals**: Set `update_interval` programmatically based on integration logic, not user input
- **Minimum Intervals**:
  - Local network: 5 seconds
  - Cloud services: 60 seconds
- **Parallel Updates**: Specify number of concurrent updates:
  ```python
  PARALLEL_UPDATES = 1  # Serialize updates to prevent overwhelming device
  # OR
  PARALLEL_UPDATES = 0  # Unlimited (for coordinator-based or read-only)
  ```

