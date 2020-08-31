# -*- coding: utf-8 -*-
from collective.fullcalendar.behaviors.fullcalendar import IFullcalendarMarker
from collective.fullcalendar.testing import \
    COLLECTIVE_FULLCALENDAR_INTEGRATION_TESTING  # noqa
from plone.app.testing import setRoles, TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class FullcalendarIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_FULLCALENDAR_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_behavior_fullcalendar(self):
        behavior = getUtility(IBehavior, 'collective.fullcalendar.fullcalendar')
        self.assertEqual(
            behavior.marker,
            IFullcalendarMarker,
        )
