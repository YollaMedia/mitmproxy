"""
Use mitmproxy's filter pattern in scripts.
"""
import typing
from mitmproxy import ctx, http
from mitmproxy.addons.defy.defyrewrite import UrlRedirectSpec, test_location


class HarFilter:
    def __init__(self):
        self.options: typing.List[UrlRedirectSpec] = []

    def configure(self, updated):
        if "harfilter" in updated:
            options = ctx.options.harfilter
            for har_filter in options:
                self.options.append(
                    UrlRedirectSpec([], har_filter)
                )

    def load(self, l):
        l.add_option("harfilter", typing.Sequence[typing.Dict], [], "Check that flow matches filter.")


harFilter = HarFilter()


def should_flow_excluded(flow: http.HTTPFlow) -> bool:
    result = False

    for har_filter in harFilter.options:
        if test_location(flow=flow, spec=har_filter):
            result = True
            break

    return result


addons = [harFilter]
