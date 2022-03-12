#!/usr/bin/env python3

### IMPORTS ###
import logging
import os

from flask import Flask, url_for

from hasts.plugins.services import BasicFileBackedObjectDatastoreService
from hasts.plugins.services import InProcessLoggingService
from hasts.plugins.services import FlaskAppService
from hasts.plugins.manager import PluginFactory

from .rootblueprint import root_blueprint, SITEMAP_LINKS

### GLOBALS ###

### FUNCTIONS ###
def setup_server():
    app = Flask(__name__)
    return app

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

### CLASSES ###
class Server:
    # This should have the plugin manager parts to load the rest of the components.
    # This should also setup the underlying services for the plugins, such as logging and datastore.
    # This should pull the information for setting up the services from environment variables and possibly config files.
    def __init__(self, flask_app):
        self.logger = logging.getLogger(type(self).__name__)
        self.logger.debug("Inputs - flask_app: %s", flask_app)
        self._flask_app = flask_app

        # Get the environs
        # FIXME: This should use the "Path" library for basic protections.
        # FIXME: Add graceful error-out if environs not set.
        # FIXME: This should come from some sort of configuration class.
        self._datastore_file = os.getenv('HASTS_DATASTORE_FILE')

        # FIXME: Should this be in the initializer, or in a setup method?
        self._services_logging = InProcessLoggingService()
        self._services_object_datastore = BasicFileBackedObjectDatastoreService(self._datastore_file)
        self._services_flask_app = FlaskAppService(self._flask_app)
        self._plugin_factory = PluginFactory(self._services_logging)
        self._plugin_factory.register_service("object_datastore", self._services_object_datastore)
        self._plugin_factory.register_service("flask_app", self._services_flask_app)

        # FIXME: Should the plugins be loaded here, or in a setup method?
        # FIXME: How should the plugins and services be specified?
        #        - Should a callback be used to trigger the plugin registration?
        #        - Should the plugin register itself to the flask_app provided in the flask_app service?
        # FIXME: Should services be able to be provided by plugins?

        self._plugin_factory.load("hasts.recipebook.plugin", "RecipeBookPlugin")

        # Register the core of the UI as the root
        self._flask_app.register_blueprint(root_blueprint)

        # Register any of the UIs for the plugins as children of the root

        # Generate the sitemap and pass to the root blueprint
        # FIXME: This is a crude way to do this using globals.  This should be
        #        cleaned up once the root blueprint is converted to a class.
        for rule in self._flask_app.url_map.iter_rules():
            # Filter out rules we can't navigate to in a browser
            # and rules that require parameters
            if "GET" in rule.methods and has_no_empty_params(rule):
                # with self._flask_app.app_context():
                #     url = url_for(rule.endpoint, **(rule.defaults or {}))
                #     SITEMAP_LINKS.append((url, rule.rule))
                self.logger.debug("SiteMap endpoint: %s, rule: %s", rule.endpoint, rule.rule)
                SITEMAP_LINKS.append(rule.rule)