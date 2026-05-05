from __future__ import annotations

import os
import os.path
from collections.abc import Iterable
from glob import glob

import importlib_resources
from tutor import hooks
from tutor.types import Config
from tutormfe.hooks import MFE_APPS, MFE_ATTRS_TYPE

from tutormfe_extensions.__about__ import __version__


def validate_mfe_config(mfe_setting_name: str) -> str | None:
    if mfe_setting_name.startswith("MFE_") and mfe_setting_name.endswith("_MFE_APP"):
        return mfe_setting_name.replace("_MFE_APP", "").replace("MFE_", "").replace("_", "-").lower()
    return None


@hooks.Actions.CONFIG_LOADED.add()
def load_config(config: Config):
    # The tutormfe.plugins.get_mfes function gets cached before we can
    # register the new list of MFES. This causes discrepancies when using
    # MFE_*_MFE_APP settings in which some templates that use the `get_mfes`
    # function will have stale values.
    #
    # Manually trigger the PLUGINS_LOADED action clears the cache.
    hooks.Actions.PLUGIN_LOADED.do("tutormfe_extensions")

    @MFE_APPS.add()
    def _manage_mfes_from_config(mfes: dict[str, MFE_ATTRS_TYPE]):
        for setting_name, setting_value in config.items():
            mfe_key = validate_mfe_config(setting_name)
            if not mfe_key:
                continue

            if setting_value is None:
                mfes.pop(mfe_key, None)
                continue

            if not isinstance(setting_value, dict):
                continue

            mfes[mfe_key] = {
                "repository": setting_value["repository"],
                "port": setting_value["port"],
            }

            if "version" in setting_value:
                mfes[mfe_key]["version"] = setting_value["version"]

        return mfes


hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        # Add your new settings that have default values here.
        # Each new setting is a pair: (setting_name, default_value).
        # Prefix your setting names with 'MFE_EXTENSIONS_'.
        ("MFE_EXTENSIONS_VERSION", __version__),
        ("MFE_EXTENSIONS_CDN_URL", ""),
        ("MFE_EXTENSIONS_BY_PATH", True),
    ]
)


def iter_mfes_per_service(service: str = "") -> Iterable[str]:
    """
    Return the list of MFEs that should be hosted via path in the
    same domain as each service.

    """
    active_mfes = MFE_APPS.apply({})
    cms_mfes = {"authoring"}
    lms_mfes = set(active_mfes) - cms_mfes

    for mfe in active_mfes:
        if service == "lms" and mfe in lms_mfes:
            yield mfe
        if service == "cms" and mfe in cms_mfes:
            yield mfe


hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    [
        str(importlib_resources.files("tutormfe_extensions") / "templates"),
    ]
)

hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    # For each pair (source_path, destination_path):
    # templates at ``source_path`` (relative to your ENV_TEMPLATE_ROOTS) will be
    # rendered to ``source_path/destination_path`` (relative to your Tutor environment).
    # For example, ``tutormfe_extensions/templates/mfe_extensions/build``
    # will be rendered to ``$(tutor config printroot)/env/plugins/mfe_extensions/build``.
    [
        ("mfe_extensions/apps", "plugins"),
        ("mfe_extensions/k8s", "plugins"),
        ("mfe/build", "plugins"),
    ],
)

# Make the mfe_extensions functions available within templates
hooks.Filters.ENV_TEMPLATE_VARIABLES.add_items(
    [
        ("iter_mfes_per_service", iter_mfes_per_service),
    ],
)

for path in glob(str(importlib_resources.files("tutormfe_extensions") / "patches" / "*")):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))
