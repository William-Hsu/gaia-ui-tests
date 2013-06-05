# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.email.app import Email


class TestSetupGmail(GaiaTestCase):

    email_configured = False

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.connect_to_network()

        self.email = Email(self.marionette)
        self.email.launch()

    def test_setup_basic_gmail(self):
        # setup basic gmail account
        self.email.basic_setup_email(self.testvars['email']['gmail']['name'],
                                     self.testvars['email']['gmail']['email'],
                                     self.testvars['email']['gmail']['password'])
        self.email_configured = True

        # check header area
        self.assertTrue(self.email.header.is_compose_visible)
        self.assertTrue(self.email.header.is_menu_visible)
        self.assertEqual(self.email.header.label, 'Inbox')

        # check toolbar area
        self.assertTrue(self.email.toolbar.is_edit_visible)
        self.assertTrue(self.email.toolbar.is_refresh_visible)

        # check account has emails
        self.email.wait_for_emails_to_sync()
        self.assertGreater(len(self.email.mails), 0)

    def tearDown(self):
        if self.email_configured:
            self.email.delete_email_account(0)
        GaiaTestCase.tearDown(self)
