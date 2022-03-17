import typing
from mitmproxy import ctx, http, exceptions
from mitmproxy.addons.defy.db import get_url_redirect

class UrlRedirectSpec(typing.NamedTuple):
    rule: str
    replacement: str

def parse_url_redirect_spec(option):
    return UrlRedirectSpec(rule=option["rule"], replacement=option["replacement"])

class DefyUrlRedirect:
    def __init__(self):
        self.replacements: typing.List[UrlRedirectSpec] = []

    def load(self, loader):
        loader.add_option(
            "url_redirect", typing.Sequence[str], [],
            """
            URL Redirect
            """
        )

    def configure(self, updated):
        if "url_redirect" in updated:
            options = get_url_redirect()
            self.replacements = []

            for option in options:
                try:
                    spec = parse_url_redirect_spec(option=option)
                except ValueError as e:
                    ctx.log.info(f"Cannot parse url_redirect option {option}: {e}")
                    # raise exceptions.OptionsError(f"Cannot parse url_redirect option {option}: {e}") from e
                    continue

                self.replacements.append(spec)

    def request(self, flow: http.HTTPFlow) -> None:
        if flow.response or flow.error or not flow.live:
            return

        for spec in self.replacements:
            if flow.request.pretty_host == spec.rule:
                flow.request.host = spec.replacement
                break

addons = [
    DefyUrlRedirect()
]

