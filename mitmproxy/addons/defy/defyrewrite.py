import re
import typing
import fnmatch

from mitmproxy import ctx, http, exceptions
from mitmproxy.addons.defy.db import get_rewrite

class UrlRedirectSpec(typing.NamedTuple):
    rule: typing.List
    location: typing.Dict

def parse_rewrite_spec(option):
    return UrlRedirectSpec(rule=option["rule"], location=option["location"])

def test_location(flow: http.HTTPFlow, spec: UrlRedirectSpec) -> bool:
    if spec.location["scheme"]:
        if not fnmatch.fnmatch(flow.request.scheme, spec.location["scheme"]):
            # ctx.log.info("Scheme not match: " + flow.request.scheme + spec.location["scheme"])
            return False

    if spec.location["host"]:
        if not fnmatch.fnmatch(flow.request.pretty_host, spec.location["host"]):
            # ctx.log.info("host not match: " + flow.request.pretty_host + spec.location["host"])
            return False

    if spec.location["port"]:
        port = int(spec.location["port"])
        if flow.request.port != port:
            # ctx.log.info("port not match: " + flow.request.port + spec.location["port"])
            return False

    if spec.location["path"]:
        if not fnmatch.fnmatch(flow.request.path, spec.location["path"]):
            # ctx.log.info("path not match: " + flow.request.path + spec.location["path"])
            return False

    # ctx.log.info(where + " Location Matched")
    return True


def test_rule_match(flow: http.HTTPFlow, rule, where):
    if not rule["enabled"]: 
        # ctx.log.info("Rule Not enabled")
        return False


    if len(rule["where"]) > 0:
        if (where not in rule["where"]):
            # ctx.log.info("reqeust / response not matched")
            return False


    if (rule["type"] in [
        'host',
        'path',
        'url',
        'add_query_param',
        'modify_query_param',
        'remove_query_param',
    ]):
        if where == 'response':
            # ctx.log.info(rule["type"] + " didn't work in response")
            return False


    if (rule["type"] in [
        'response_status',
    ]):
        if where == 'request':
            # ctx.log.info(rule["type"] + " didn't work in request")
            return False


    # case_sensitive

    # if [
    #     'modify_header',
    #     'remove_header',
    # ].index(rule["type"]) > -1:
    #     return False

    # if [
    #     'modify_query_param',
    #     'remove_query_param',
    # ].index(rule["type"]) > -1:
    #     return False
    # ctx.log.info(where + " Rule Matched")

    return True


def str_replacement(content, search, replacement, case_sensitive, replace_all, is_regex, match_whole_value = False):
    if replace_all:
        is_regex = True

    if not case_sensitive:
        is_regex = True

    if is_regex:
        if case_sensitive:
            pattern = re.compile(search, re.IGNORECASE)
        else:
            pattern = re.compile(search)

        if replace_all:
            return pattern.sub(lambda m: replacement, content)
        else:
            return pattern.sub(lambda m: replacement, content, 1)
        # return pattern.sub(replacement, content)
        # return re.sub('(?i)'+re.escape(old), lambda m: repl, text)
    else:
        return content.replace(search, replacement)


def request_replacement(flow: http.HTTPFlow, rule):
    if rule["type"] == 'add_header':
        if not hasattr(flow.response.headers, rule["replace"]["name"]):
            if rule["replace"]["name"]:
                flow.response.headers[rule["replace"]["name"]] = rule["replace"]["value"]

    if rule["type"] == 'modify_header':
        pass
    if rule["type"] == 'remove_header':
        if hasattr(flow.response.headers, rule["replace"]["name"]):
            del flow.response.headers[rule["match"]["name"]]

    if rule["type"] == 'host':
        host = str_replacement(
            content=flow.request.pretty_host,
            search=rule["match"]["value"],
            replacement=rule["replace"]["value"],
            case_sensitive=False,
            replace_all=False,
            is_regex=rule["match"]["is_value_regex"],
        )
        if flow.request.pretty_host != host:
            flow.request.host = host

    if rule["type"] == 'path':
        path = str_replacement(
            content=flow.request.path,
            search=rule["match"]["value"],
            replacement=rule["replace"]["value"],
            case_sensitive=False,
            replace_all=True,
            is_regex=rule["match"]["is_value_regex"],
        )
        if flow.request.path != path:
            flow.request.path = path

    if rule["type"] == 'url':
        url = str_replacement(
            content=flow.request.url,
            search=rule["match"]["value"],
            replacement=rule["replace"]["value"],
            case_sensitive=False,
            replace_all=True,
            is_regex=rule["match"]["is_value_regex"],
        )
        if flow.request.url != url:
            # replace schema host page
            pass
    if rule["type"] == 'add_query_param':
        pass
    if rule["type"] == 'modify_query_param':
        pass
    if rule["type"] == 'remove_query_param':
        pass
    if rule["type"] == 'body':
        pass



def response_replacement(flow: http.HTTPFlow, rule):
    if rule["type"] == 'add_header':
        if not hasattr(flow.response.headers, rule["replace"]["name"]):
            if rule["replace"]["name"]:
                flow.response.headers[rule["replace"]["name"]] = rule["replace"]["value"]

    if rule["type"] == 'modify_header':
        pass
    if rule["type"] == 'remove_header':
        if hasattr(flow.response.headers, rule["replace"]["name"]):
            del flow.response.headers[rule["match"]["name"]]

    if rule["type"] == 'response_status':
        pass
    if rule["type"] == 'body':
        try:
            text = str_replacement(
                content = flow.response.text, 
                search = rule["match"]["value"], 
                replacement = rule["replace"]["value"], 
                case_sensitive = rule["match"]["case_sensitive"], 
                replace_all = rule["replace"]["replace_all"],
                is_regex= rule["match"]["is_value_regex"],
            )

            flow.response.text = text
        except:
            pass

        # ctx.log.info(flow.response.encoding)
        # ctx.log.info(flow.response.content)
        # ctx.log.info("text " + flow.request.get_text())


class DefyRewrite:
    def __init__(self):
        self.replacements: typing.List[UrlRedirectSpec] = []

    def load(self, loader):
        loader.add_option(
            "rewrite", typing.Sequence[str], [],
            """
            URL Redirect
            """
        )

    def configure(self, updated):
        if "rewrite" in updated:
            options = get_rewrite()
            self.replacements = []

            for option in options:
                try:
                    spec = parse_rewrite_spec(option=option)
                except ValueError as e:
                    ctx.log.info(f"Cannot parse rewrite option {option}: {e}")
                    # raise exceptions.OptionsError(f"Cannot parse rewrite option {option}: {e}") from e
                    continue
                except Exception as e:
                    ctx.log.info(f"Exception {option}: {e}")

                self.replacements.append(spec)


    def request(self, flow: http.HTTPFlow) -> None:
        if flow.response or flow.error or not flow.live:
            return

        for spec in self.replacements:
            if test_location(flow=flow, spec=spec):
                for rule in spec.rule:
                    if test_rule_match(flow=flow, rule=rule, where="request"):
                        request_replacement(flow=flow, rule=rule)


    def response(self, flow: http.HTTPFlow) -> None:
        for spec in self.replacements:
            if test_location(flow=flow, spec=spec):
                for rule in spec.rule:
                    if test_rule_match(flow=flow, rule=rule, where="response"):
                        response_replacement(flow=flow, rule=rule)


addons = [
    DefyRewrite()
]
