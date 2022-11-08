import logging
from mitmproxy import ctx, hooks
from mitmproxy.addons.defy.utils.maplocal import reset_map_local
from mitmproxy.addons.defy.utils.mapremote import reset_map_remote


# def _get_name(itm):
#     return getattr(itm, "name", itm.__class__.__name__.lower())

def configure_addon(config):
    addon_names = []
    logging.info("reloading config...")
    # logging.info(config)

    if "map_local" in config:
        logging.info("reloading map_local...")
        reset_map_local(config["map_local"])
        addon_names.append("map_local")

    if "map_remote" in config:
        logging.info("reloading map_remote...")
        reset_map_remote(config["map_remote"])
        addon_names.append("map_remote")

    if "url_redirect" in config:
        logging.info("reloading url_redirect...")
        ctx.options.url_redirect = config["url_redirect"]
        addon_names.append("url_redirect")

    if "rewrite" in config:
        logging.info("reloading rewrite...")
        ctx.options.rewrite = config["rewrite"]
        addon_names.append("rewrite")

    if "harfilter" in config:
        logging.info("reloading harfilter...")
        ctx.options.harfilter = config["harfilter"]
        addon_names.append("harfilter")

    if len(addon_names) > 0:
        logging.info("reloading config...")
        logging.info(addon_names)
        ctx.master.addons.trigger(hooks.ConfigureHook(addon_names))


# def reset_addon():
#     for addon in self.addons.chain:
#         logging.info(_get_name(addon))
#     addon = ctx.master.addons.get("browserupaddonsmanageraddon")
#     addon.configure_addon()