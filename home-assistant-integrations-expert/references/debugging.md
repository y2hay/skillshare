## Debugging & Troubleshooting

### Common Issues & Solutions
- **Integration won't load**: Check `manifest.json` syntax and required fields
- **Entities not appearing**: Verify `unique_id` and `has_entity_name` implementation
- **Config flow errors**: Check `strings.json` entries and error handling
- **Discovery not working**: Verify manifest discovery configuration and callbacks
- **Tests failing**: Check mock setup and async context

### Debug Logging Setup
```python
# Enable debug logging in tests
caplog.set_level(logging.DEBUG, logger="my_integration")

# In integration code - use proper logging
_LOGGER = logging.getLogger(__name__)
_LOGGER.debug("Processing data: %s", data)  # Use lazy logging
```

### Validation Commands
```bash
# Check specific integration
python -m script.hassfest --integration-path homeassistant/components/my_integration

# Validate quality scale
# Check quality_scale.yaml against current rules

# Run integration tests with coverage
pytest ./tests/components/my_integration \
  --cov=homeassistant.components.my_integration \
  --cov-report term-missing
```
