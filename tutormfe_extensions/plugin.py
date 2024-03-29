from __future__ import annotations

import os
import os.path
from glob import glob

import click
import pkg_resources
from tutor import config as tutor_config
from tutor import hooks
from tutormfe.hooks import MFE_APPS


from .__about__ import __version__

########################################
# CONFIGURATION
########################################

CORE_MFES_CONFIG = {
    "MFE_LEARNING_MFE_APP": {
        "name": "learning",
        "repository": "https://github.com/eduNEXT/frontend-app-learning",
        "port": 2000,
        "version": "ednx-release/palma.master",
    },
    "MFE_ACCOUNT_MFE_APP": {
        "name": "account",
        "repository": "https://github.com/eduNEXT/frontend-app-account",
        "port": 1997,
        "version": "ednx-release/palma.master",
    },
    "MFE_AUTHN_MFE_APP": {
        "name": "authn",
        "repository": "https://github.com/eduNEXT/frontend-app-authn",
        "port": 1999,
        "version": "ednx-release/palma.master",
    },
    "MFE_DISCUSSIONS_MFE_APP": {
        "name": "discussions",
        "repository": "https://github.com/eduNEXT/frontend-app-discussions",
        "port": 2002,
        "version": "ednx-release/palma.master",
    },
    "MFE_GRADEBOOK_MFE_APP": {
        "name": "gradebook",
        "repository": "https://github.com/eduNEXT/frontend-app-gradebook",
        "port": 1994,
        "version": "ednx-release/palma.master",
    },
    "MFE_PROFILE_MFE_APP": {
        "name": "profile",
        "repository": "https://github.com/eduNEXT/frontend-app-profile",
        "port": 1995,
        "version": "ednx-release/palma.master",
    },
    "MFE_ORA_GRADING_MFE_APP": {
        "name": "ora-grading",
        "repository": "https://github.com/eduNEXT/frontend-app-ora-grading",
        "port": 2003,
        "version": "ednx-release/palma.master",
    },
    "MFE_COMMUNICATIONS_MFE_APP": {
        "name": "communications",
        "repository": "https://github.com/eduNEXT/frontend-app-communications",
        "port": 2004,
        "version": "ednx-release/palma.master",
    }
}

def validate_mfe_config(mfe_setting_name: str):
    if mfe_setting_name.startswith("MFE_") and mfe_setting_name.endswith("_MFE_APP"):
        return (
            mfe_setting_name
            .replace("_MFE_APP", "")
            .replace("MFE_", "")
            .replace("_", "-")
            .lower()
        )
    return None

@MFE_APPS.add()
def _manage_mfes_from_config(mfe_list):
    config = tutor_config.load('.')
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

hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        # Add settings that don't have a reasonable default for all users here.
        # For instance: passwords, secret keys, etc.
        # Each new setting is a pair: (setting_name, unique_generated_value).
        # Prefix your setting names with 'MFE_EXTENSIONS_'.
        # For example:
        ### ("MFE_EXTENSIONS_SECRET_KEY", "{{ 24|random_string }}"),
    ]
)

hooks.Filters.CONFIG_OVERRIDES.add_items(
    [
        # Danger zone!
        # Add values to override settings from Tutor core or other plugins here.
        # Each override is a pair: (setting_name, new_value). For example:
        (k,v) for k,v in CORE_MFES_CONFIG.items()
    ]
)

########################################
# INITIALIZATION TASKS
########################################

# To add a custom initialization task, create a bash script template under:
# tutormfe_extensions/templates/mfe_extensions/jobs/init/
# and then add it to the MY_INIT_TASKS list. Each task is in the format:
# ("<service>", ("<path>", "<to>", "<script>", "<template>"))
MY_INIT_TASKS: list[tuple[str, tuple[str, ...]]] = [
    # For example, to add LMS initialization steps, you could add the script template at:
    # tutormfe_extensions/templates/mfe_extensions/jobs/init/lms.sh
    # And then add the line:
    ### ("lms", ("mfe_extensions", "jobs", "init", "lms.sh")),
]


# For each task added to MY_INIT_TASKS, we load the task template
# and add it to the CLI_DO_INIT_TASKS filter, which tells Tutor to
# run it as part of the `init` job.
for service, template_path in MY_INIT_TASKS:
    full_path: str = pkg_resources.resource_filename(
        "tutormfe_extensions", os.path.join("templates", *template_path)
    )
    with open(full_path, encoding="utf-8") as init_task_file:
        init_task: str = init_task_file.read()
    hooks.Filters.CLI_DO_INIT_TASKS.add_item((service, init_task))


########################################
# DOCKER IMAGE MANAGEMENT
########################################


# Images to be built by `tutor images build`.
# Each item is a quadruple in the form:
#     ("<tutor_image_name>", ("path", "to", "build", "dir"), "<docker_image_tag>", "<build_args>")
hooks.Filters.IMAGES_BUILD.add_items(
    [
        # To build `myimage` with `tutor images build myimage`,
        # you would add a Dockerfile to templates/mfe_extensions/build/myimage,
        # and then write:
        ### (
        ###     "myimage",
        ###     ("plugins", "mfe_extensions", "build", "myimage"),
        ###     "docker.io/myimage:{{ MFE_EXTENSIONS_VERSION }}",
        ###     (),
        ### ),
    ]
)


# Images to be pulled as part of `tutor images pull`.
# Each item is a pair in the form:
#     ("<tutor_image_name>", "<docker_image_tag>")
hooks.Filters.IMAGES_PULL.add_items(
    [
        # To pull `myimage` with `tutor images pull myimage`, you would write:
        ### (
        ###     "myimage",
        ###     "docker.io/myimage:{{ MFE_EXTENSIONS_VERSION }}",
        ### ),
    ]
)


# Images to be pushed as part of `tutor images push`.
# Each item is a pair in the form:
#     ("<tutor_image_name>", "<docker_image_tag>")
hooks.Filters.IMAGES_PUSH.add_items(
    [
        # To push `myimage` with `tutor images push myimage`, you would write:
        ### (
        ###     "myimage",
        ###     "docker.io/myimage:{{ MFE_EXTENSIONS_VERSION }}",
        ### ),
    ]
)


########################################
# TEMPLATE RENDERING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    # Root paths for template files, relative to the project root.
    [
        pkg_resources.resource_filename("tutormfe_extensions", "templates"),
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


########################################
# PATCH LOADING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

# For each file in tutormfe_extensions/patches,
# apply a patch based on the file's name and contents.
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutormfe_extensions", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))


########################################
# CUSTOM JOBS (a.k.a. "do-commands")
########################################

# A job is a set of tasks, each of which run inside a certain container.
# Jobs are invoked using the `do` command, for example: `tutor local do importdemocourse`.
# A few jobs are built in to Tutor, such as `init` and `createuser`.
# You can also add your own custom jobs:

# To add a custom job, define a Click command that returns a list of tasks,
# where each task is a pair in the form ("<service>", "<shell_command>").
# For example:
### @click.command()
### @click.option("-n", "--name", default="plugin developer")
### def say_hi(name: str) -> list[tuple[str, str]]:
###     """
###     An example job that just prints 'hello' from within both LMS and CMS.
###     """
###     return [
###         ("lms", f"echo 'Hello from LMS, {name}!'"),
###         ("cms", f"echo 'Hello from CMS, {name}!'"),
###     ]


# Then, add the command function to CLI_DO_COMMANDS:
## hooks.Filters.CLI_DO_COMMANDS.add_item(say_hi)

# Now, you can run your job like this:
#   $ tutor local do say-hi --name="Moisés González"


#######################################
# CUSTOM CLI COMMANDS
#######################################

# Your plugin can also add custom commands directly to the Tutor CLI.
# These commands are run directly on the user's host computer
# (unlike jobs, which are run in containers).

# To define a command group for your plugin, you would define a Click
# group and then add it to CLI_COMMANDS:


### @click.group()
### def mfe_extensions() -> None:
###     pass


### hooks.Filters.CLI_COMMANDS.add_item(mfe_extensions)


# Then, you would add subcommands directly to the Click group, for example:


### @mfe_extensions.command()
### def example_command() -> None:
###     """
###     This is helptext for an example command.
###     """
###     print("You've run an example command.")


# This would allow you to run:
#   $ tutor mfe_extensions example-command
