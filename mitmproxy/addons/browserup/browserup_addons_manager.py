import _thread
import asyncio
import json

import falcon
import os
import logging

from wsgiref.simple_server import make_server
from pathlib import Path
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from falcon_apispec import FalconPlugin
from mitmproxy.addons.browserup.har.har_schemas import MatchCriteriaSchema, VerifyResultSchema, ErrorSchema, CounterSchema
from mitmproxy.addons.browserup.har_capture_addon import HarCaptureAddOn
from mitmproxy import ctx


class BrowserUpAddonsManagerAddOn:
    initialized = False

    def load(self, l):
        logging.info('Loading BrowserUpAddonsManagerAddOn')
        l.add_option(
            "addons_management_port", int, 8088, "REST api management port.",
        )

    def running(self):
        logging.info('Scanning for custom add-ons resources...')
        global initialized
        if not self.initialized and self.is_script_loader_initialized():
            logging.info('Scanning for custom add-ons resources...')
            logging.info('Starting falcon REST service...')
            _thread.start_new_thread(self.start_falcon, ())
            initialized = True

    def is_script_loader_initialized(self):
        script_loader = ctx.master.addons.get("scriptloader")

        for custom_addon in script_loader.addons:
            if len(custom_addon.addons) == 0:
                return False

        return True

    def basic_spec(self, app):
        return APISpec(
            title='BrowserUp MitmProxy',
            version='1.0.0',
            servers = [{"url": "http://localhost:{port}/",
                        "description": "The development API server",
                        "variables": {"port": {"enum": ["8088"], "default": '8088'}}
                        }],
            tags = [{"name": 'The BrowserUp MitmProxy API', "description": "BrowserUp MitmProxy REST API"}],
            info= {"description":
                   """___
This is the REST API for controlling the BrowserUp MitmProxy.
The BrowserUp MitmProxy is a swiss army knife for automated testing that
captures HTTP traffic in HAR files. It is also useful for Selenium/Cypress tests.
___
""", "x-logo": {"url": "logo.png"}},
            openapi_version='3.0.3',
            plugins=[
                FalconPlugin(app),
                MarshmallowPlugin(),
            ],
        )

    def write_spec(self, spec):
        pretty_json = json.dumps(spec.to_dict(), indent=2)
        root = Path(__file__).parent.parent.parent.parent
        schema_path = os.path.join(root, 'browserup-proxy.schema.json')
        f = open(schema_path, 'w')
        f.write(pretty_json)
        f.close()

    def load_resources_from_addons(self, app, spec):
        # Whenever the addons manager loads, we write out our openapi spec
        # There might be a better place for this, although where isn't clear to me yet
        addons = ctx.master.addons
        resources = []
        get_resources_fun_name = "get_resources"
        for custom_addon in addons.chain:
            if hasattr(custom_addon, get_resources_fun_name):
                addon_resources = getattr(custom_addon, get_resources_fun_name)()
                for resource in addon_resources:
                    route = "/" + resource.addon_path()
                    app.add_route(route, resource)
                    if 'apispec' in dir(resource):
                        resource.apispec(spec)
                    resources.append(resource)
        return resources

    def get_app(self):
        app = falcon.API()
        spec = self.basic_spec(app)
        spec.components.schema('MatchCriteria', schema=MatchCriteriaSchema)
        spec.components.schema('VerifyResult', schema=VerifyResultSchema)
        spec.components.schema('Error', schema=ErrorSchema)
        spec.components.schema('Counter', schema=CounterSchema)
        self.load_resources_from_addons(app, spec)
        self.write_spec(spec)
        return app

    def get_all_routes(self, app):
        routes_list = []

        def get_children(node):
            if len(node.children):
                for child_node in node.children:
                    get_children(child_node)
            else:
                routes_list.append((node.uri_template, node.resource))
        [get_children(node) for node in app._router._roots]
        return routes_list

    def start_falcon(self):
        app = self.get_app()
        print("Routes: ")
        print(self.get_all_routes(app))
        with make_server('', ctx.options.addons_management_port, app) as httpd:
            print('Starting REST API management on port: {}'.format(ctx.options.addons_management_port))
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            httpd.serve_forever()

            # https://marshmallow.readthedocs.io/en/stable/quickstart.html


addons = [
    HarCaptureAddOn(),
    BrowserUpAddonsManagerAddOn()
]
