# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestYouTube(GaiaTestCase):

    # Firefox/chrome locators
    _awesome_bar_locator = ("id", "url-input")
    _url_button_locator = ("id", "url-button")
    _throbber_locator = ("id", "throbber")
    _browser_frame_locator = ('css selector', 'iframe[mozbrowser]')

    # Video player fullscreen
    _video_frame_locator = ('css selector', "iframe[src^='app://video'][src$='view.html']")
    _video_spinner_locator = ('id', 'spinner-overlay')
    _video_player_locator = ('id', 'player')
    _video_player_frame_locator = ('id', 'videoFrame')
    _video_loaded_locator = ('css selector', 'video[style]')

    # YouTube
    _video_container_locator = ('id', 'koya_elem_0_6')
    _video_URL = 'http://m.youtube.com/watch?v=5MzuGWFIfio'

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.connect_to_network()
        self.app = self.apps.launch('Browser')
        self.wait_for_condition(lambda m: m.execute_script("return window.wrappedJSObject.Browser.hasLoaded;"))

    def test_play_youtube_video(self):
        """ Confirm YouTube video playback

        https://moztrap.mozilla.org/manage/case/6073/

        """

        awesome_bar = self.marionette.find_element(*self._awesome_bar_locator)
        awesome_bar.send_keys(self._video_URL)

        url_button = self.marionette.find_element(*self._url_button_locator)
        self.marionette.tap(url_button)

        self.wait_for_condition(lambda m: not self.is_browser_throbber_visible())

        browser_frame = self.marionette.find_element(
            *self._browser_frame_locator)

        self.marionette.switch_to_frame(browser_frame)

        # Tap the video
        self.wait_for_element_present(*self._video_container_locator)
        video = self.marionette.find_element(*self._video_container_locator)

        self.marionette.tap(video)

        # Switch to video player
        self.marionette.switch_to_frame()
        self.wait_for_element_present(*self._video_frame_locator)
        self.marionette.switch_to_frame(self.marionette.find_element(*self._video_frame_locator))

        # Wait for the video and player to load
        self.wait_for_condition(lambda m: self.is_video_throbber_not_visible())
        self.wait_for_element_displayed(*self._video_player_frame_locator)
        self.wait_for_element_displayed(*self._video_loaded_locator)

        # Check for playback
        self.assertTrue(self.is_video_playing())

    def is_browser_throbber_visible(self):
        return self.marionette.find_element(*self._throbber_locator).get_attribute('class') == 'loading'

    def is_video_throbber_not_visible(self):
        return self.marionette.find_element(*self._video_spinner_locator).get_attribute('class') == 'hidden'

    def is_video_playing(self):
        return self.marionette.find_element(*self._video_player_locator).get_attribute('paused') == 'false'
