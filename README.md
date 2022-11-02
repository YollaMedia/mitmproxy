## Development Setup

### Install:
```
python3 -m venv venv
venv/bin/pip install -e ".[dev]"
```


### VS Code setting:
Config `.vscode/settings.json`:

```
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv",
    "python.linting.flake8Enabled": true,
    "python.linting.enabled": true,
    "python.formatting.provider": "black"
}
```


### Upgrade:
```
python3.10 -m pip install --upgrade pip
```


### Active virtualenv

```
source venv/bin/activate
mitmdump --version
```


### Run

Verify that the command work:

```
mitmdump --set confdir=./.mitmproxy
```


Installl cert files(optional)


Start service:
```
browserup-proxy --set confdir=./.mitmproxy
```


## Testing

### RUn Python tests

```
tox -e py
```

or:

```
cd test/mitmproxy/addons
pytest --cov mitmproxy.addons.anticache --cov-report term-missing --looponfail test_anticache.py
```


### Code Style

```
tox -e flake8
```

