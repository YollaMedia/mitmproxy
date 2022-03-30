from mitmproxy import ctx, http, exceptions
from mitmproxy.addons.defy.defyrewrite import UrlRedirectSpec, test_location


har_filters = []

har_entry_include_hosts = [
    "www.google-analytics.com",
    "securepubads.g.doubleclick.net",
    "portal.cdn.yollamedia.com",
    "*.yollamedia.com",
    "ssc.33across.com",
    "ssc-cms.33across.com",
    "yolla-d.openx.net",
    "*.apx.appier.net",
    "*.bfmio.com",
    "player-cdn.beachfrontmedia.com",
    "web.hb.ad.cpe.dotomi.com",
    "dmx.districtm.io",
    "g2.gumgum.com",
    "htlb.casalemedia.com",
    "*.indexww.com",
    "*.openx.net",
    "bid.contextweb.com",
    "tag.1rx.io",
    "*.rubiconproject.com",
    "ap.lijit.com",
    "tlx.3lift.com",
    "ssc.33across.com",
]

for host in har_entry_include_hosts:
    har_filters.append(
        UrlRedirectSpec([], {
            "scheme": "",
            "host": host,
            "port": "",
            "path": "",
        })
    )


def should_flow_excluded(flow: http.HTTPFlow) -> bool:
    result = False

    for har_filter in har_filters:
        if test_location(flow=flow, spec=har_filter):
            result = True
            break

    if result:
        return False
    else:
        return True
