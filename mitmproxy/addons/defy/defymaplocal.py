from mitmproxy import ctx, hooks
from mitmproxy.addons.defy.db import dbclient


def get_temporary_mapping_data():
    new_list=[]
    temporary_mapping_data = dbclient["mitm"]["map_local"].find()

    for temporary_mapping in temporary_mapping_data:
        # ctx.log.info(temporary_mapping)
        if temporary_mapping["enabled"] and temporary_mapping["rule"]:
            temporary_mapping["rule"] = temporary_mapping["rule"] + "|" + temporary_mapping["file_path"]
            # remove path from temporary_mapping
            new_list.append(temporary_mapping)

    return new_list



def reset_map_local():
    map_local = get_temporary_mapping_data()

    # if ctx.options.map_local is None:
    #     ctx.options.map_local = []
    # else:
    #     ctx.options.map_local.clear()

    map_local_rule = []

    for option in map_local:
        ctx.log.info(option["rule"])
        map_local_rule.append(option["rule"])
        # ctx.options.map_local.append(option["rule"])
    
    ctx.options.map_local = map_local_rule
    # ctx.master.addons.trigger(hooks.ConfigureHook(["map_local"]))

    return "map_local"

    # ao_map_local = ctx.master.addons.get("map_local")
    # ctx.log.info(ao_map_local)
