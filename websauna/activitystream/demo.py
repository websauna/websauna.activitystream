"""This contains app entry point for running a demo site for this addon or running functional tests for this addon."""

import websauna.system
from websauna.system.model.meta import Base

from .renderer import DefaultActivityRenderer, register_activity_renderer


class Initializer(websauna.system.DemoInitializer):
    """A demo / test app initializer for testing addon websauna.activitystream."""

    def include_addons(self):
        """Include this addon in the configuration."""
        self.config.include("websauna.activitystream")

    def configure_views(self):
        super(Initializer, self).configure_views()

        from . import demoapp
        self.config.scan(demoapp)

        # Register out test renderer
        register_activity_renderer(self.config.registry, demoapp.DemoMessageRenderer, "demo_msg")

        self.config.add_jinja2_search_path('websauna.activitystream:demotemplates', name='.html', prepend=True)


def main(global_config, **settings):
    init = Initializer(global_config)
    init.run()
    return init.make_wsgi_app()
