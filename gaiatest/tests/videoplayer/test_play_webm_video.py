# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.videoplayer.app import VideoPlayer


class TestPlayWebMVideo(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)

        # add video to storage
        self.push_resource('VID_0001.webm', destination='DCIM/100MZLLA')

    def test_play_webm_video(self):
        """https://moztrap.mozilla.org/manage/case/2478/"""

        video_player = VideoPlayer(self.marionette)
        video_player.launch()

        # Assert that there is at least one video available
        self.assertGreater(video_player.total_video_count, 0)

        first_video_name = video_player.first_video_name

        # Click on the first video
        fullscreen_video = video_player.tap_first_video_item()

        # Video will play automatically
        # Tap on the toolbar to keep it visible
        fullscreen_video.tap_control_bar()

        # The elapsed time != 0:00 is the only indication of the toolbar visible
        self.assertNotEqual(fullscreen_video.elapsed_time, '00:00')

        # Check the name too. This will only work if the toolbar is visible
        self.assertEqual(first_video_name, fullscreen_video.name)
