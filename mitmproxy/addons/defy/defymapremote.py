from mitmproxy import ctx, hooks
from mitmproxy.addons.defy.db import dbclient


def get_temporary_mapping_data():
    new_list=[]
    temporary_mapping_data = dbclient["mitm"]["map_remote"].find()

    for temporary_mapping in temporary_mapping_data:
        if temporary_mapping["enabled"] and temporary_mapping["rule"]:
            new_list.append(temporary_mapping)

    return new_list


def reset_map_remote():
    map_remote = get_temporary_mapping_data()
    map_remote_rule = []

    for option in map_remote:
        ctx.log.info(option["rule"])
        map_remote_rule.append(option["rule"])
    
    ctx.options.map_remote = map_remote_rule
    # ctx.master.addons.trigger(hooks.ConfigureHook(["map_remote"]))

    return "map_remote"
