# -*- coding: utf-8 -*-
from . import logger
from .base import reload_gs_profile
from Products.CMFCore.utils import getToolByName
# from plone import api


def remove_csscompilation_keys(context):
    """Removes the csscompilation key from the registry."""
    registry = getToolByName(context, "portal_registry")
    key_to_remove = "plone.bundles/fullcalendar-main.csscompilation"

    if key_to_remove in registry.records:
        del registry.records[key_to_remove]
        logger.info(f"Removed registry key: {key_to_remove}")


def upgrade(setup_tool=None):
    """Run upgrade to FullCalendar v6."""

    logger.info("Running upgrade (Python): Upgrade to FullCalendar v6")
    reload_gs_profile(setup_tool)
    remove_csscompilation_keys(setup_tool)
