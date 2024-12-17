from __future__ import annotations

import os
import os.path
from glob import glob
from typing import Iterable

import importlib_resources
from tutor import config as tutor_config
from tutor import hooks
from tutormfe.hooks import MFE_APPS
from tutormfe.plugin import CORE_MFE_APPS


from .__about__ import __version__

########################################
# CONFIGURATION
########################################

CORE_MFES_CONFIG = {}


def validate_mfe_config(mfe_setting_name: str):
    if mfe_setting_name.startswith("MFE_") and mfe_setting_name.endswith("_MFE_APP"):
        return (
            mfe_setting_name.replace("_MFE_APP", "")
            .replace("MFE_", "")
            .replace("_", "-")
            .lower()
        )
    return None


@MFE_APPS.add()
def _manage_mfes_from_config(mfe_list):
    config = tutor_config.load(".")
    for setting, value in config.items():
        mfe_name = validate_mfe_config(setting)
        if not mfe_name:
            continue

        if value is None:
            mfe_list.pop(mfe_name)
            continue

        mfe_defaults = CORE_MFES_CONFIG.get(setting, {})
        mfe_defaults.update(value)

        mfe_list[mfe_defaults["name"]] = {
            "repository": mfe_defaults["repository"],
            "port": mfe_defaults["port"],
            "version": mfe_defaults["version"],
        }

    return mfe_list


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
    lms_mfes = set(CORE_MFE_APPS) - cms_mfes

    for mfe in active_mfes:
        if service == "lms" and mfe in lms_mfes:
            yield mfe
        if service == "cms" and mfe in cms_mfes:
            yield mfe


########################################
# TEMPLATE RENDERING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    # Root paths for template files, relative to the project root.
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

########################################
# PATCH LOADING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

# For each file in tutormfe_extensions/patches,
# apply a patch based on the file's name and contents.
for path in glob(
    os.path.join(
        str(importlib_resources.files("tutormfe_extensions") / "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))
