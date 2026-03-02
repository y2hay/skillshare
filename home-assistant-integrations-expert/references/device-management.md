## Device Management

### Device Registry
- **Create Devices**: Group related entities under devices
- **Device Info**: Provide comprehensive metadata:
  ```python
  _attr_device_info = DeviceInfo(
      connections={(CONNECTION_NETWORK_MAC, device.mac)},
      identifiers={(DOMAIN, device.id)},
      name=device.name,
      manufacturer="My Company",
      model="My Sensor",
      sw_version=device.version,
  )
  ```
- For services: Add `entry_type=DeviceEntryType.SERVICE`

### Dynamic Device Addition
- **Auto-detect New Devices**: After initial setup
- **Implementation Pattern**:
  ```python
  def _check_device() -> None:
      current_devices = set(coordinator.data)
      new_devices = current_devices - known_devices
      if new_devices:
          known_devices.update(new_devices)
          async_add_entities([MySensor(coordinator, device_id) for device_id in new_devices])

  entry.async_on_unload(coordinator.async_add_listener(_check_device))
  ```

### Stale Device Removal
- **Auto-remove**: When devices disappear from hub/account
- **Device Registry Update**:
  ```python
  device_registry.async_update_device(
      device_id=device.id,
      remove_config_entry_id=self.config_entry.entry_id,
  )
  ```
- **Manual Deletion**: Implement `async_remove_config_entry_device` when needed

### Entity Categories
- **Required**: Assign appropriate category to entities
- **Implementation**: Set `_attr_entity_category`
  ```python
  class MySensor(SensorEntity):
      _attr_entity_category = EntityCategory.DIAGNOSTIC
  ```
- Categories include: `DIAGNOSTIC` for system/technical information

### Device Classes
- **Use When Available**: Set appropriate device class for entity type
  ```python
  class MyTemperatureSensor(SensorEntity):
      _attr_device_class = SensorDeviceClass.TEMPERATURE
  ```
- Provides context for: unit conversion, voice control, UI representation

### Disabled by Default
- **Disable Noisy/Less Popular Entities**: Reduce resource usage
  ```python
  class MySignalStrengthSensor(SensorEntity):
      _attr_entity_registry_enabled_default = False
  ```
- Target: frequently changing states, technical diagnostics

### Entity Translations
- **Required with has_entity_name**: Support international users
- **Implementation**:
  ```python
  class MySensor(SensorEntity):
      _attr_has_entity_name = True
      _attr_translation_key = "phase_voltage"
  ```
- Create `strings.json` with translations:
  ```json
  {
    "entity": {
      "sensor": {
        "phase_voltage": {
          "name": "Phase voltage"
        }
      }
    }
  }
  ```

### Exception Translations (Gold)
- **Translatable Errors**: Use translation keys for user-facing exceptions
- **Implementation**:
  ```python
  raise ServiceValidationError(
      translation_domain=DOMAIN,
      translation_key="end_date_before_start_date",
  )
  ```
- Add to `strings.json`:
  ```json
  {
    "exceptions": {
      "end_date_before_start_date": {
        "message": "The end date cannot be before the start date."
      }
    }
  }
  ```

### Icon Translations (Gold)
- **Dynamic Icons**: Support state and range-based icon selection
- **State-based Icons**:
  ```json
  {
    "entity": {
      "sensor": {
        "tree_pollen": {
          "default": "mdi:tree",
          "state": {
            "high": "mdi:tree-outline"
          }
        }
      }
    }
  }
  ```
- **Range-based Icons** (for numeric values):
  ```json
  {
    "entity": {
      "sensor": {
        "battery_level": {
          "default": "mdi:battery-unknown",
          "range": {
            "0": "mdi:battery-outline",
            "90": "mdi:battery-90",
            "100": "mdi:battery"
          }
        }
      }
    }
  }
  ```

