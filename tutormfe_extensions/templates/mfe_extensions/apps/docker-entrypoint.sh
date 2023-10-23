#!/bin/sh
find /openedx/dist/ -type f -exec sed -i -e "s|MFE_EXTENSIONS_PLACEHOLDER_STRING|$MFE_CDN_URL|g" {} \;
exec $@
