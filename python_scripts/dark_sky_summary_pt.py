state = hass.states.get('sensor.dark_sky_summary').state
response = os.system('curl --data "key=trnsl.1.1.20180312T184049Z.25ec68dcb8cdd93c.e8313f4eb494259e59ca6a6efd1c03e42e81d8a6&lang=en-pt&text=' + state + '" https://translate.yandex.net/api/v1.5/tr.json/translate')
hass.states.set('input_text.dark_sky_summary_pt',response.json()['text'][0])