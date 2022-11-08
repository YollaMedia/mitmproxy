import logging
from mitmproxy import ctx, hooks
# from mitmproxy.addons.defy.db import get_map_remote


def reset_map_remote(map_remote):
    # map_remote = get_map_remote()
    map_remote_rule = []

    for option in map_remote:
        # logging.info("[Map Remote] " + option["description"])
        # map_remote_rule.append(option["rule"])
        logging.info("[Map Remote] " + option)
        map_remote_rule.append(option)
    
    ctx.options.map_remote = map_remote_rule
    # ctx.master.addons.trigger(hooks.ConfigureHook(["map_remote"]))

    return "map_remote"