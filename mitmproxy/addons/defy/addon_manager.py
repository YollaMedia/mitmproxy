from mitmproxy import ctx, hooks
from mitmproxy.addons.defy.defymaplocal import reset_map_local
from mitmproxy.addons.defy.defymapremote import reset_map_remote

# def _get_name(itm):
#     return getattr(itm, "name", itm.__class__.__name__.lower())

#YMPB
def configure_addon(config):
    addon_names = []
    ctx.log.info("reloading config...")
    # ctx.log.info(config)

    if "map_local" in config:
        ctx.log.info("reloading map_local...")
        reset_map_local(config["map_local"])
        addon_names.append("map_local")

    if "map_remote" in config:
        ctx.log.info("reloading map_remote...")
        reset_map_remote(config["map_remote"])
        addon_names.append("map_remote")

    if "url_redirect" in config:
        ctx.log.info("reloading url_redirect...")
        ctx.options.url_redirect = config["url_redirect"]
        addon_names.append("url_redirect")

    if "rewrite" in config:
        ctx.log.info("reloading rewrite...")
        ctx.options.rewrite = config["rewrite"]
        addon_names.append("rewrite")

    if len(addon_names) > 0:
        ctx.log.info("reloading config...")
        ctx.log.info(addon_names)
        ctx.master.addons.trigger(hooks.ConfigureHook(addon_names))


# def reset_addon():
#     for addon in self.addons.chain:
#         ctx.log.info(_get_name(addon))
#     addon = ctx.master.addons.get("browserupaddonsmanageraddon")
#     addon.configure_addon()