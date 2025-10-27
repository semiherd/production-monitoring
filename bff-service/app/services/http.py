import requests
def urljoin(base, path):
    base = base.rstrip('/'); path = path.lstrip('/'); return f"{base}/{path}"
def post(base, path, json=None, headers=None, timeout=10):
    return requests.post(urljoin(base, path), json=json, headers=headers or {}, timeout=timeout)
def get(base, path, headers=None, timeout=10, params=None, stream=False):
    return requests.get(urljoin(base, path), headers=headers or {}, timeout=timeout, params=params, stream=stream)
