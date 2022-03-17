from mitmproxy import ctx, hooks
from mitmproxy.addons.defy.defymaplocal import reset_map_local
from mitmproxy.addons.defy.defymapremote import reset_map_remote

# def _get_name(itm):
#     return getattr(itm, "name", itm.__class__.__name__.lower())

#YMPB
def configure_addon():
    addon_names = []
    addon_names.append(reset_map_local())
    addon_names.append(reset_map_remote())

    addon_names.append("url_redirect")

    ctx.master.addons.trigger(hooks.ConfigureHook(addon_names))


# def reset_addon():
#     for addon in self.addons.chain:
#         ctx.log.info(_get_name(addon))
#     addon = ctx.master.addons.get("browserupaddonsmanageraddon")
#     addon.configure_addon()