# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import collective.fullcalendar


class CollectiveFullcalendarLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.fullcalendar)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.fullcalendar:default")


COLLECTIVE_FULLCALENDAR_FIXTURE = CollectiveFullcalendarLayer()


COLLECTIVE_FULLCALENDAR_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_FULLCALENDAR_FIXTURE,),
    name="CollectiveFullcalendarLayer:IntegrationTesting",
)


COLLECTIVE_FULLCALENDAR_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_FULLCALENDAR_FIXTURE,),
    name="CollectiveFullcalendarLayer:FunctionalTesting",
)


COLLECTIVE_FULLCALENDAR_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_FULLCALENDAR_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="CollectiveFullcalendarLayer:AcceptanceTesting",
)
