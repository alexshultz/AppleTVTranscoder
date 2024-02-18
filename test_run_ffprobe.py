import Setup
import unittest
from unittest.mock import patch, Mock
from MediaFile import MediaFile


class TestRunFfprobe(unittest.TestCase):

    def test_run_ffprobe_valid_json(self):
        # Arrange
        mock_result = Mock()
        mock_result.stdout = '{"streams": [{"width": 1920, "height": 1080}]}'
        with patch('subprocess.run', return_value=mock_result):
            media_file = MediaFile(Setup.TEST_VIDEO_FILE)
            command = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'json', 'test_file.mp4']

            # Act
            result = media_file.run_ffprobe(command)

            # Assert
            self.assertEqual(result, {"streams": [{"width": 1920, "height": 1080}]})


if __name__ == '__main__':
    unittest.main()
