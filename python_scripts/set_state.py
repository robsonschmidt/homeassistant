entity = data.get('entity')
logger.warning(entity)
hass.states.set(entity,'off')

