# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base


class SetupEmail(Base):

    _name_locator = ('css selector', 'input.sup-info-name')
    _email_locator = ('css selector', 'input.sup-info-email')
    _password_locator = ('css selector', 'input.sup-info-password')
    _next_locator = ('css selector', '.sup-info-next-btn')
    _continue_button_locator = ('class name', 'sup-show-mail-btn sup-form-btn recommend')

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.wait_for_element_displayed(*self._name_locator)

    def type_name(self, value):
        self.marionette.find_element(*self._name_locator).send_keys(value)

    def type_email(self, value):
        self.marionette.find_element(*self._email_locator).send_keys(value)

    def type_password(self, value):
        self.marionette.find_element(*self._password_locator).send_keys(value)

    def tap_next(self):
        self.marionette.tap(self.marionette.find_element(*self._next_locator))

    def wait_for_setup_complete(self):
        self.wait_for_element_displayed(*self._continue_button_locator)

    def tap_continue(self):
        self.marionette.tap(self.marionette.find_element(*self._continue_button_locator))
