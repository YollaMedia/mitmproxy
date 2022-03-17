from mitmproxy import ctx, hooks
from mitmproxy.addons.defy.db import get_map_remote


def reset_map_remote():
    map_remote = get_map_remote()
    map_remote_rule = []

    for option in map_remote:
        ctx.log.info(option["rule"])
        map_remote_rule.append(option["rule"])
    
    ctx.options.map_remote = map_remote_rule
    # ctx.master.addons.trigger(hooks.ConfigureHook(["map_remote"]))

    return "map_remote"
