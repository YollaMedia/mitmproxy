from mitmproxy import ctx, hooks
# from mitmproxy.addons.defy.db import get_map_local

def reset_map_local(map_local):
    # map_local = get_map_local()

    # if ctx.options.map_local is None:
    #     ctx.options.map_local = []
    # else:
    #     ctx.options.map_local.clear()

    map_local_rule = []

    for option in map_local:
        ctx.log.info("[Map Local] " + option["description"])
        map_local_rule.append(option["rule"])
        # ctx.options.map_local.append(option["rule"])
    
    ctx.options.map_local = map_local_rule
    # ctx.master.addons.trigger(hooks.ConfigureHook(["map_local"]))

    return "map_local"

    # ao_map_local = ctx.master.addons.get("map_local")
    # ctx.log.info(ao_map_local)
