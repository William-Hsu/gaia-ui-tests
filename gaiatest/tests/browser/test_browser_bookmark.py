# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.browser.app import Browser


class TestBrowserBookmark(GaiaTestCase):

    _homescreen_frame_locator = ('css selector', 'div.homescreen > iframe')
    _homescreen_icon_locator = ('css selector', 'li.icon[aria-label="%s"]')
    _bookmark_added = False

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.connect_to_network()

        import time
        curr_time = repr(time.time()).replace('.', '')
        self.bookmark_title = 'gaia%s' % curr_time[10:]
        self._homescreen_icon_locator = (self._homescreen_icon_locator[0],
                                         self._homescreen_icon_locator[1] % self.bookmark_title)

    def test_browser_bookmark(self):
        # https://github.com/mozilla/gaia-ui-tests/issues/452
        browser = Browser(self.marionette)
        browser.launch()

        browser.go_to_url('http://mozqa.com/data/firefox/layout/mozilla.html')

        browser.tap_bookmark_button()
        browser.tap_add_bookmark_to_home_screen_choice_button()
        browser.type_bookmark_title(self.bookmark_title)
        browser.tap_add_bookmark_to_home_screen_dialog_button()

        # Switch to Home Screen to look for bookmark
        self.marionette.switch_to_frame()
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('home'));")
        self.marionette.switch_to_frame(self.marionette.find_element(*self._homescreen_frame_locator))

        # Wait for Gaia to insert the element into the page
        self.wait_for_element_present(*self._homescreen_icon_locator)

        # check whether bookmark was added
        while self._homescreen_has_more_pages:
            if self.is_element_displayed(*self._homescreen_icon_locator):
                self._bookmark_added = True
                break
            self._go_to_next_page()

        self.assertTrue(self._bookmark_added, 'The bookmark %s was not found to be installed on the home screen.' % self.bookmark_title)

    def tearDown(self):
        if self._bookmark_added:
            self._delete_bookmark(self.bookmark_title)

        GaiaTestCase.tearDown(self)

    def _go_to_next_page(self):
        self.marionette.execute_script('window.wrappedJSObject.GridManager.goToNextPage()')

    @property
    def _homescreen_has_more_pages(self):
        # the naming of this could be more concise when it's in an app object!
        return self.marionette.execute_script("""
        var pageHelper = window.wrappedJSObject.GridManager.pageHelper;
        return pageHelper.getCurrentPageNumber() < (pageHelper.getTotalPagesNumber() - 1);""")

    def _delete_bookmark(self, bookmark_name):
        # TODO move this snippet to the Homescreen app object

        # ensure we are in the homescreen app
        self.apps.launch('Homescreen')
        self.marionette.execute_script("""
                                          name = arguments[0];
                                          let apps = window.wrappedJSObject.GridManager.getApps();
                                          apps.forEach (function(aApp) {
                                            if (aApp.isBookmark) {
                                              if (aApp.manifest.name == name) {
                                                console.log('uninstalling app with name ' + aApp.manifest.name);
                                                window.wrappedJSObject.GridManager.uninstall(aApp);
                                              };
                                            };
                                          });
                                        """, script_args=[bookmark_name])
