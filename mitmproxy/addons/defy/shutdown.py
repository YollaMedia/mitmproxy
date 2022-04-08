from mitmproxy import ctx, http
from mitmproxy.options import CONF_DIR

def request(flow: http.HTTPFlow) -> None:
    # a random condition to make this example a bit more interactive
    if flow.request.pretty_url == "http://example.com/path":
        ctx.log.info("Shutting down everything...")

        # CONF_DIR
        flow.request.data

        addon = ctx.master.addons.get("browserupaddonsmanageraddon")
        addon.httpd.shutdown()
        addon.loop.stop()
        ctx.master.shutdown()

        raise Exception("shutdown")
