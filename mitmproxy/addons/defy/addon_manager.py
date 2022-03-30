from mitmproxy import ctx, hooks
from mitmproxy.addons.defy.defymaplocal import reset_map_local
from mitmproxy.addons.defy.defymapremote import reset_map_remote

# def _get_name(itm):
#     return getattr(itm, "name", itm.__class__.__name__.lower())

#YMPB
def configure_addon(config):
    ctx.log.info("reloading config...")
    addon_names = []

    reset_map_local(config["map_local"])
    addon_names.append("map_local")

    reset_map_remote(config["map_remote"])
    addon_names.append("map_remote")

    ctx.options.url_redirect = config["url_redirect"]
    addon_names.append("url_redirect")

    ctx.options.rewrite = config["rewrite"]
    addon_names.append("rewrite")

    ctx.master.addons.trigger(hooks.ConfigureHook(addon_names))


# def reset_addon():
#     for addon in self.addons.chain:
#         ctx.log.info(_get_name(addon))
#     addon = ctx.master.addons.get("browserupaddonsmanageraddon")
#     addon.configure_addon()