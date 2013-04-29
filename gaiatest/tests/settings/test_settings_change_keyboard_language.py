# -*- coding: UTF-8 -*-
# This is Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestChangeKeyboardLanguage(GaiaTestCase):

    # Language settings locators
    _keyboard_settings_locator = ("id", "menuItem-keyboard")
    _select_language_locator   = ("xpath", "//section[@id='keyboard']//li/label[input[@name='keyboard.layouts.spanish']]")
    _select_text_field_locator = ("css selector", "input[type='text']")
    _select_keyb_frame_locator = ("css selector", "#keyboard-frame iframe")
    _language_key_locator      = ("css selector", ".keyboard-row button[data-keycode='-3']")
    _special_key_locator       = ("css selector", ".keyboard-row button[data-keycode='241']")
    _specific_key              = u'\xf1'

    def setUp(self):
        GaiaTestCase.setUp(self)

        # Launch the Settings app
        self.app = self.apps.launch('Settings')

    def test_change_keyboard_language_settings(self):

        # Navigate to keyboard settings
        self.wait_for_element_present(*self._keyboard_settings_locator)
        keyboard_setting = self.marionette.find_element(*self._keyboard_settings_locator)

        # Select keyboard setting
        self.marionette.execute_script("arguments[0].scrollIntoView(false);", [keyboard_setting])
        self.marionette.tap(keyboard_setting)

        # Select keyboard language
        self.wait_for_element_present(*self._select_language_locator)
        selected_language = self.marionette.find_element(*self._select_language_locator)
        import pdb; pdb.set_trace()
        self.marionette.tap(selected_language)


        # --Verify the keyboard layout
        # --launch the email app (follow manyally test case)
        self.app = self.apps.launch('email')

        # Select name field
        self.wait_for_element_present(*self._select_text_field_locator)
        select_text_field = self.marionette.find_element(*self._select_text_field_locator)
        # tap() cannot work here
        select_text_field.click()

        # Switch to keyboard frame and change language -> Temporary solution. Waiting for keyboard class
        self.marionette.switch_to_frame()
        keybframe = self.marionette.find_element(*self._select_keyb_frame_locator)
        self.marionette.switch_to_frame(keybframe, focus=False)

        # Temporary solution since action-chain function not yet merged
        language_key = self.marionette.find_element(*self._language_key_locator)
        self.marionette.tap(language_key)
        special_key = self.marionette.find_element(*self._special_key_locator).text

        # Checking if exists the special key - "ñ"
        self.assertEqual(special_key, self._specific_key)
