import urllib.parse

DEFAULT_BASE_URL = 'https://webservice.wikipathways.org'

def wikipathways_get(operation, parameters=None, format='json', base_url=DEFAULT_BASE_URL):
    try:
        url = build_url(base_url, operation)
        r = requests.request('GET', url, params=parameters)
        r.raise_for_status()
        try:
            return r.json()
        except ValueError as e:
            if require_json:
                raise
            else:
                return r.text
    except requests.exceptions.RequestException as e:
        _handle_error(e)

def build_url(base_url=DEFAULT_BASE_URL, operation=None):
    if operation is not None:
        return base_url + "/" + urllib.parse.quote(operation)
    else:
        return base_url
