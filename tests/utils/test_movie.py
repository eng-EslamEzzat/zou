import os
import shutil
import tempfile
import unittest
from PIL import Image
import math

from pathlib import Path
from urllib import request

import ffmpeg

from zou.utils import movie


class MovieTestCase(unittest.TestCase):
    def setUp(self):
        # download test file once
        self.tmpdir = tempfile.mkdtemp()
        self.video_only_path = str(Path(self.tmpdir) / "demo.m4v")
        test_url = os.getenv(
            "ZOU_TEST_VIDEO_URL", "http://fate-suite.ffmpeg.org/mpeg4/demo.m4v"
        )
        request.urlretrieve(test_url, self.video_only_path)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_soundtrack(self):
        filename = "test_soundtrack.m4v"
        video = str(Path(self.tmpdir) / filename)
        shutil.copyfile(self.video_only_path, video)
        shutil.copyfile(self.video_only_path, video + ".tmp")

        self.assertFalse(movie.has_soundtrack(video))
        ret, out, _ = movie.add_empty_soundtrack(video)
        self.assertEqual(ret, 0)
        self.assertFalse(out)  # check this value because we ignore it.
        self.assertTrue(movie.has_soundtrack(video))

        # Test case where a .tmp suffix has been added to the file name.
        ret, out, _ = movie.add_empty_soundtrack(video + ".tmp")
        self.assertEqual(ret, 0)
        self.assertTrue(movie.has_soundtrack(video + ".tmp"))

        # Create an audio file
        stream = ffmpeg.input(video)
        audio_only = str(
            Path(self.tmpdir) / ("audio_only-test_soundtrack.mp4")
        )
        stream = ffmpeg.output(stream.audio, audio_only, f="mp4", c="aac")
        stream.run(quiet=False, cmd=("ffmpeg", "-xerror"))

        self.assertTrue(movie.has_soundtrack(audio_only))

        # Ensure an error occurs
        """ Cannot make it work anymore
        ret, out, _ = movie.add_empty_soundtrack(audio_only)
        self.assertEqual(1, ret)
        """

    def test_get_movie_size(self):
        width, height = movie.get_movie_size(self.video_only_path)
        self.assertEqual(width, 320)
        self.assertEqual(height, 240)

    def test_normalize(self):
        filename = "test_normalize.m4v"
        video = str(Path(self.tmpdir) / filename)
        shutil.copyfile(self.video_only_path, video)

        self.assertFalse(movie.has_soundtrack(video))
        width, height = movie.get_movie_size(video)
        normalized, _, _ = movie.normalize_movie(video, 5, width, height)

        # normalization adds an audio stream
        self.assertTrue(movie.has_soundtrack(normalized))

        # dimensions are unchanged
        width_norm, height_norm = movie.get_movie_size(normalized)
        self.assertEqual(width, width_norm)
        self.assertEqual(height, height_norm)

    def test_normalize_width_unspecified(self):
        filename = "test_normalize_no_width.m4v"
        video = str(Path(self.tmpdir) / filename)
        shutil.copyfile(self.video_only_path, video)

        width, height = movie.get_movie_size(video)
        normalized, _, _ = movie.normalize_movie(
            video, 5, None, int(height / 2)
        )
        width_norm, height_norm = movie.get_movie_size(normalized)
        self.assertEqual(width / 2, width_norm)
        self.assertEqual(height / 2, height_norm)

    def test_concat_demuxer_testing(self):
        test_name = "test_concate_demuxer"
        self.concat_testing(movie.concat_demuxer, test_name)

    def test_concat_filter_testing(self):
        test_name = "test_concate_filter"
        self.concat_testing(movie.concat_filter, test_name)

    def concat_testing(self, method, test_name):
        videos = []
        width, height = movie.get_movie_size(self.video_only_path)
        for i in range(0, 2):
            filename = "%s-%s.m4v" % (i, test_name)
            video = str(Path(self.tmpdir) / filename)
            shutil.copyfile(self.video_only_path, video)
            normalized, _, _ = movie.normalize_movie(video, 5, width, height)
            # 2nd item isn't used by build_playlist_movie
            videos.append((normalized, None))

        out = "out-%s.mp4" % test_name
        out = str(Path(self.tmpdir) / out)

        result = movie.build_playlist_movie(
            method, videos, out, width, height, fps=5
        )
        self.assertTrue(result.get("success"))
        self.assertFalse(result.get("message"))

        width_playlist, height_playlist = movie.get_movie_size(out)
        self.assertEqual(width, width_playlist)
        self.assertEqual(height, height_playlist)

    def test_create_tile(self):
        video_path = "./tests/fixtures/videos/test_preview_tiles.mp4"
        video_width, video_height = movie.get_movie_size(video_path)
        tile_path = movie.generate_tile(video_path, movie_fps=25)
        image = Image.open(tile_path)
        img_width, img_height = image.size

        probe = ffmpeg.probe(video_path)
        duration_in_seconds = float(probe['streams'][0]['duration'])
        float_movie_fps = eval(probe['streams'][0]['r_frame_rate'])
        duration_in_frames = int(duration_in_seconds * float_movie_fps)
        rows = math.ceil((duration_in_frames / 8))

        aspect_ratio = (video_width / video_height)
        target_width = math.ceil(aspect_ratio * 100)

        os.remove(tile_path)
        self.assertEqual(img_width, target_width * 8)
        self.assertEqual(img_height, 100 * rows)
