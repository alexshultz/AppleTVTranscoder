import unittest
from unittest.mock import MagicMock
from MediaFile import MediaFile  # Replace with the actual module name


class TestGetBitrate(unittest.TestCase):
    def test_get_bitrate_calculates_correctly(self):
        # Create an instance of the MediaFile class
        media_file = MediaFile("/Users/alex/Downloads/themediacenterinaction.mp4")

        # Mock the ffprobe method to return a specific value
        media_file.run_ffprobe = MagicMock(return_value={"format": {"bit_rate": 1000}})

        # Call the method you want to test
        result = media_file.get_bitrate()

        # Make assertions based on the expected behavior
        self.assertEqual(result, 1)


if __name__ == '__main__':
    unittest.main()
