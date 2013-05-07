# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.marketplace.app import Marketplace


class TestMarketplaceLogin(GaiaTestCase):

    MARKETPLACE_DEV_NAME = 'Marketplace Dev'

    # Marketplace locators
    _settings_button_locator = ('css selector', 'a.header-button.settings')
    _sign_in_button_locator = ('css selector', 'a.button.browserid')
    _signed_in_notification_locator = ('id', 'notification')
    _sign_out_button_locator = ('css selector', 'a.button.logout')

    _email_account_field_locator = ('id', 'email')

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.connect_to_network()
        self.install_marketplace()

        self.marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        self.marketplace.launch()

    def test_login_marketplace(self):
        # https://moztrap.mozilla.org/manage/case/4134/

        self.marketplace.wait_for_setting_displayed()
        settings = self.marketplace.tap_settings()
        persona = settings.tap_sign_in()

        persona.login(self.testvars['marketplace']['username'], self.testvars['marketplace']['password'])

        # switch back to Marketplace
        self.marionette.switch_to_frame()
        self.marketplace.launch()

        # tap on the signed-in notification at the bottom of the screen to dismiss it
        self.wait_for_element_displayed(*self._signed_in_notification_locator)
        self.marionette.tap(self.marionette.find_element(*self._signed_in_notification_locator))

        settings.wait_for_sign_out_button()

        # Verify that user is logged in
        self.assertEqual(self.testvars['marketplace']['username'], settings.email)

        # Sign out, which should return to the Marketplace home screen
        settings.tap_sign_out()

        # Verify that user is signed out
        self.marketplace.wait_for_setting_displayed()
        settings = self.marketplace.tap_settings()
        settings.wait_for_sign_in_displayed()
