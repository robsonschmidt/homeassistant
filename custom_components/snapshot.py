DOMAIN = 'snapshot'

def setup(hass, config):
    hass.states.set('hello.world', 'Paulus')

    return True