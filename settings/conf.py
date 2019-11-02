from goodconf import GoodConf, Value


class Config(GoodConf):
    """Configuration settings for College Conductor"""

    DEBUG = Value(default=False, help="Toggle debugging.")


config = Config(default_files=["/etc/conductor/settings.yaml", "settings.yaml"])
