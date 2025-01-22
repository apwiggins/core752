"""
Simple example custom service, used to drive shell commands on a node.
Install at ~/.core/myservices/
"""
from typing import Tuple

from core.nodes.base import CoreNode
from core.services.coreservices import CoreService, ServiceMode


class PIMDM(CoreService):
    name: str = "PIMDM"
    group: str = "Multicast"
    dirs: Tuple[str, ...] = (
        "/usr/local/etc/pimdd", 
        "/var/log/pimdd",
        "/usr/local/var/run",
        "/usr/local/var/log",
        )
    configs: Tuple[str, ...] = (
        "/usr/local/etc/pimdd/pimdd.conf",
        "pimdd.sh",
        )
    startup: Tuple[str, ...] = ("bash pimdd.sh",)
    shutdown: Tuple[str, ...] = ("killall pimdd",)
    validate: Tuple[str, ...] = ("pidof pimdd",)

    @classmethod
    def generate_config(cls, node: CoreNode, filename: str) -> str:
        """
        Return the pimdd.conf or quaggaboot.sh file contents.
        """
        if filename == cls.configs[0]:
            return cls.generate_pimddconf(node)
        elif filename == cls.configs[1]:
            return cls.generate_pimdd_boot(node)
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
    def generate_pimddconf(cls, node: CoreNode) -> str:
        """
        Returns a string representation for a file, given the node the service is
        starting on the config filename that this information will be used for. This
        must be defined, if "configs" are defined.

        :param node: core node that the service is being ran on
        :param filename: configuration file to generate
        :return: configuration file content
        """
        cfg = "#   This is the configuration file for pimd, an IP multicast router.\n"
        cfg += "#   pimd looks for it in /usr/local/etc/pimdd/pimdd.conf.\n"
        cfg += "#   Command formats:\n"
        cfg += "# default_source_preference [preference]\n"
        cfg += "# default_source_metric metric\n"
        cfg += "# phyint [local-addr] [disable] | preference [preference] metric [metric] igmpgateway\n"
        cfg += "\n"
        cfg += "# By default PIM will be activated on all interfaces.  Use phyint to \n"
        cfg += "# disable on interfaces where PIM should not be run.\n"
        cfg += "\n"
        cfg += "#default_source_preference 131\n"
        cfg += "#default_source_metric 20\n"
        cfg += "#phyint 128.223.91.129 localpref 101\n"
        cfg += "#phyint 128.223.163.129 disable\n"
        cfg += "#phyint 1.1.1.1 igmpgateway\n"
        cfg += "#phyint 10.0.0.2 disable\n"
        cfg += "\n### interfaces found by PIMDD service\n"
        for iface in node.get_ifaces():
            cfg += f'phyint {iface.name} enable\n'
        return cfg

    @classmethod
    def generate_pimdd_boot(cls, node: CoreNode) -> str:
        """
        Returns a string representation for a file, given the node the service is
        starting on the config filename that this information will be used for. This
        must be defined, if "configs" are defined.

        :param node: core node that the service is being ran on
        :param filename: configuration file to generate
        :return: configuration file content
        """
        cfg = "#!/bin/sh\n"
        cfg += "### default command and debug flags for pimdd\n"
        cfg += "### unmark debug flags as needed\n"
        cfg += "### use tail -f pim_log.txt to watch pimdd live debug output from stderr\n"
        cfg += "/usr/local/sbin/pimdd -f /usr/local/etc/pimdd/pimdd.conf -w 5"

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
