## Entity Development

### Unique IDs
- **Required**: Every entity must have a unique ID for registry tracking
- Must be unique per platform (not per integration)
- Don't include integration domain or platform in ID
- **Implementation**:
  ```python
  class MySensor(SensorEntity):
      def __init__(self, device_id: str) -> None:
          self._attr_unique_id = f"{device_id}_temperature"
  ```

**Acceptable ID Sources**:
- Device serial numbers
- MAC addresses (formatted using `format_mac` from device registry)
- Physical identifiers (printed/EEPROM)
- Config entry ID as last resort: `f"{entry.entry_id}-battery"`

**Never Use**:
- IP addresses, hostnames, URLs
- Device names
- Email addresses, usernames

### Entity Descriptions
- **Lambda/Anonymous Functions**: Often used in EntityDescription for value transformation
- **Multiline Lambdas**: When lambdas exceed line length, wrap in parentheses for readability
- **Bad pattern**:
  ```python
  SensorEntityDescription(
      key="temperature",
      name="Temperature",
      value_fn=lambda data: round(data["temp_value"] * 1.8 + 32, 1) if data.get("temp_value") is not None else None,  # ❌ Too long
  )
  ```
- **Good pattern**:
  ```python
  SensorEntityDescription(
      key="temperature",
      name="Temperature",
      value_fn=lambda data: (  # ✅ Parenthesis on same line as lambda
          round(data["temp_value"] * 1.8 + 32, 1)
          if data.get("temp_value") is not None
          else None
      ),
  )
  ```

### Entity Naming
- **Use has_entity_name**: Set `_attr_has_entity_name = True`
- **For specific fields**:
  ```python
  class MySensor(SensorEntity):
      _attr_has_entity_name = True
      def __init__(self, device: Device, field: str) -> None:
          self._attr_device_info = DeviceInfo(
              identifiers={(DOMAIN, device.id)},
              name=device.name,
          )
          self._attr_name = field  # e.g., "temperature", "humidity"
  ```
- **For device itself**: Set `_attr_name = None`

### Event Lifecycle Management
- **Subscribe in `async_added_to_hass`**:
  ```python
  async def async_added_to_hass(self) -> None:
      """Subscribe to events."""
      self.async_on_remove(
          self.client.events.subscribe("my_event", self._handle_event)
      )
  ```
- **Unsubscribe in `async_will_remove_from_hass`** if not using `async_on_remove`
- Never subscribe in `__init__` or other methods

### State Handling
- Unknown values: Use `None` (not "unknown" or "unavailable")
- Availability: Implement `available()` property instead of using "unavailable" state

### Entity Availability
- **Mark Unavailable**: When data cannot be fetched from device/service
- **Coordinator Pattern**:
  ```python
  @property
  def available(self) -> bool:
      """Return if entity is available."""
      return super().available and self.identifier in self.coordinator.data
  ```
- **Direct Update Pattern**:
  ```python
  async def async_update(self) -> None:
      """Update entity."""
      try:
          data = await self.client.get_data()
      except MyException:
          self._attr_available = False
      else:
          self._attr_available = True
          self._attr_native_value = data.value
  ```

### Extra State Attributes
- All attribute keys must always be present
- Unknown values: Use `None`
- Provide descriptive attributes

