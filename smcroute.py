"""
SMCroute service
"""
from typing import Tuple

from core.nodes.base import CoreNode
from core.services.coreservices import CoreService, ServiceMode


class SMCRoute(CoreService):
    name: str = "SMCRoute"
    group: str = "Multicast"
    dirs: Tuple[str, ...] = (
        "/usr/local/etc/smcroute", 
        "/var/log/smcroute",
        "/usr/local/var/run",
        "/usr/local/var/log",
        )
    configs: Tuple[str, ...] = (
        "/usr/local/etc/smcroute/smcroute.conf",
        "smcroute.sh",
        )
    startup: Tuple[str, ...] = ("bash smcroute.sh",)
    shutdown: Tuple[str, ...] = ("killall smcrouted",)
    validate: Tuple[str, ...] = ("pidof smcrouted",)

    @classmethod
    def generate_config(cls, node: CoreNode, filename: str) -> str:
        """
        Return the smcroute.conf or smcroute.sh file contents.
        """
        if filename == cls.configs[0]:
            return cls.generate_smcrouteconf(node)
        elif filename == cls.configs[1]:
            return cls.generate_smcroute_boot(node)
        else:
            raise ValueError(
                "file name (%s) is not a known configuration: %s", filename, cls.configs
            )


    @classmethod
    def on_load(cls) -> None:
        """
        Provides a way to run some arbitrary logic when the service is loaded, possibly
        to help facilitate dynamic settings for the environment.

        :return: nothing
        """
        pass

    @classmethod
    def get_configs(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the config files from the node a service
        will run. Defaults to the class definition and can be left out entirely if not
        needed.

        :param node: core node that the service is being ran on
        :return: tuple of config files to create
        """
        return cls.configs

    @classmethod
    def generate_smcrouteconf(cls, node: CoreNode) -> str:
        """
        Returns a string representation for a file, given the node the service is
        starting on the config filename that this information will be used for. This
        must be defined, if "configs" are defined.

        :param node: core node that the service is being ran on
        :param filename: configuration file to generate
        :return: configuration file content
        """
        cfg = "#   This is the configuration file for smcroute, an IP multicast router.\n"
        cfg += "#   smcroute looks for it in /usr/local/etc/smcroute/smcroute.conf.\n"
        cfg += "#   https://github.com/troglobit/smcroute\n"
        cfg += "#phyint eth0 enable mrdisc\n"
        cfg += "#phyint eth1 enable\n"
        cfg += "#phyint eth2 enable\n"
        cfg += "#mgroup from eth0 group 225.1.2.3\n"
        cfg += "#mroute from eth0 group 225.1.2.3 to eth1 eth2\n"
        cfg += "\n### interfaces found by SMCRoute service\n"
        for iface in node.get_ifaces():
            cfg += f'phyint {iface.name} enable\n'
        return cfg

    @classmethod
    def generate_smcroute_boot(cls, node: CoreNode) -> str:
        """
        Returns a string representation for a file, given the node the service is
        starting on the config filename that this information will be used for. This
        must be defined, if "configs" are defined.

        :param node: core node that the service is being ran on
        :param filename: configuration file to generate
        :return: configuration file content
        """
        cfg = "#!/bin/sh\n"
        cfg += "### default command and debug flags for SMCRoute\n"
        cfg += "/usr/local/sbin/smcrouted \\ \n"
        cfg += "\t-N \\ \n"
        cfg += "\t-e /usr/local/etc/smcroute/smcroute.conf"

        return cfg


    @classmethod
    def get_startup(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the startup commands from the node a
        service will run. Defaults to the class definition and can be left out entirely
        if not needed.

        :param node: core node that the service is being ran on
        :return: tuple of startup commands to run
        """
        return cls.startup

    @classmethod
    def get_validate(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the validate commands from the node a
        service will run. Defaults to the class definition and can be left out entirely
        if not needed.

        :param node: core node that the service is being ran on
        :return: tuple of commands to validate service startup with
        """
        return cls.validate