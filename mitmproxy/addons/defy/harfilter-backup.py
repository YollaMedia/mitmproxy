# from mitmproxy import ctx, http, exceptions
# from mitmproxy.addons.defy.defyrewrite import UrlRedirectSpec, test_location


# har_filters = []

# # TODO: add to option
# har_entry_include_hosts = [
#     "www.google-analytics.com",
#     "securepubads.g.doubleclick.net",
#     "portal.cdn.yollamedia.com",
#     "*.yollamedia.com",
#     "ssc.33across.com",
#     "ssc-cms.33across.com",
#     "yolla-d.openx.net",
#     "*.apx.appier.net",
#     "*.bfmio.com",
#     "player-cdn.beachfrontmedia.com",
#     "web.hb.ad.cpe.dotomi.com",
#     "dmx.districtm.io",
#     "g2.gumgum.com",
#     "htlb.casalemedia.com",
#     "*.indexww.com",
#     "*.openx.net",
#     "bid.contextweb.com",
#     "tag.1rx.io",
#     "*.rubiconproject.com",
#     "ap.lijit.com",
#     "tlx.3lift.com",
#     "ssc.33across.com",
# ]

# for host in har_entry_include_hosts:
#     har_filters.append(
#         UrlRedirectSpec([], {
#             "scheme": "",
#             "host": host,
#             "port": "",
#             "path": "",
#         })
#     )


# def should_flow_excluded(flow: http.HTTPFlow) -> bool:
#     result = False

#     for har_filter in har_filters:
#         if test_location(flow=flow, spec=har_filter):
#             result = True
#             break

#     if result:
#         return False
#     else:
#         return True



"""
Use mitmproxy's filter pattern in scripts.
"""
import logging
import typing
from mitmproxy import ctx, http
from mitmproxy import flowfilter


class HarFilter:
    def __init__(self):
        self.options: typing.List[flowfilter.TFilter] = []

    def configure(self, updated):
        if "harfilter" in updated:
            self.options.append(flowfilter.parse(ctx.options.harfilter))

    def load(self, l):
        l.add_option("harfilter", str, "", "Check that flow matches filter.")


harFilter = HarFilter()

def should_flow_excluded(flow: http.HTTPFlow) -> bool:
    result = False

    for har_filter in harFilter.options:
        if flowfilter.match(flow=flow, spec=har_filter):
            result = True
            break

    return result


addons = [harFilter]
