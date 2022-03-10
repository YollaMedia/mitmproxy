import re
import typing

from mitmproxy import ctx, exceptions, flowfilter, http
from mitmproxy.utils.spec import parse_spec

from mitmproxy.addons.defy.db import dbclient


class DefyMapRemoteSpec(typing.NamedTuple):
    matches: flowfilter.TFilter
    subject: str
    replacement: str


def get_temporary_mapping_data():
    new_list=[]
    temporary_mapping_data = dbclient["mitm"]["map_remote"].find()

    for temporary_mapping in temporary_mapping_data:
        new_list.append(temporary_mapping)
    return new_list


def parse_map_remote_spec(option: str) -> DefyMapRemoteSpec:
    spec = DefyMapRemoteSpec(*parse_spec(option))

    try:
        re.compile(spec.subject)
    except re.error as e:
        raise ValueError(f"Invalid regular expression {spec.subject!r} ({e})")

    return spec


class DefyMapRemote:
    def __init__(self):
        self.replacements: typing.List[DefyMapRemoteSpec] = []

    def load(self, loader):
        ctx.log.info('Loading DefyMapRemoteAddOn')
    #     loader.add_option(
    #         "map_remote", typing.Sequence[str], [],
    #         """
    #         Map remote resources to another remote URL using a pattern of the form
    #         "[/flow-filter]/url-regex/replacement", where the separator can
    #         be any character.
    #         """
    #     )

    def configure(self, updated):
        ctx.log.info('Config DefyMapRemoteAddOn')

        mapping_list = get_temporary_mapping_data()

        self.replacements = []
        for option in mapping_list:
            if option and option["enabled"] and option["rule"]:
                ctx.log.info(option["rule"])
                try:
                    spec = parse_map_remote_spec(option["rule"])
                except ValueError as e:
                    raise exceptions.OptionsError(f"Cannot parse map_remote option {option}: {e}") from e
                
                self.replacements.append(spec)


    def request(self, flow: http.HTTPFlow) -> None:
        if flow.response or flow.error or not flow.live:
            return
        for spec in self.replacements:
            if spec.matches(flow):
                url = flow.request.pretty_url
                new_url = re.sub(spec.subject, spec.replacement, url)
                # this is a bit messy: setting .url also updates the host header,
                # so we really only do that if the replacement affected the URL.
                if url != new_url:
                    flow.request.url = new_url  # type: ignore


addons = [
    DefyMapRemote()
]
