# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase

class TestBluetooth(GaiaTestCase):

    def test_bt_enabled_and_disabled(self):
        self.data_layer.bt_enable_bluetooth()
        self.assertTrue(self.data_layer.bt_is_bluetooth_enabled)

        self.data_layer.bt_disable_bluetooth()
        self.assertFalse(self.data_layer.bt_is_bluetooth_enabled)
