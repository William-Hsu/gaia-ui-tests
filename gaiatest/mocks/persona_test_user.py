#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import urllib2
import json
from gaiatest.mocks.mock_user import MockUser


class PersonaTestUser:
    """A base test class that can be extended by other tests to include utility methods."""

    def create_user(self, verified=False):
        if verified:
            url = "http://personatestuser.org/email/"
        else:
            url = "http://personatestuser.org/unverified_email/"

        response = urllib2.urlopen(url).read()
        decode = json.loads(response)

        return MockUser(email=decode['email'], password=decode['pass'], name=decode['email'].split('@')[0])
