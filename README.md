# Video Transcoding System for Apple Devices

This project provides a comprehensive solution for transcoding video files to the H.265 format, optimized for playback on Apple devices. It leverages the efficiency of H.265 to reduce file sizes while maintaining high video quality. The system is designed to run on a network of Apple Silicon Macs, processing video files stored on a NAS.

## Features

- **Two-Pass Encoding**: Utilizes two-pass encoding with `ffmpeg` to optimize video quality and compression.
- **Dynamic Resolution Handling**: Automatically downscales 4K videos to 1080p, adjusting resolution based on the original video.
- **Track Preservation**: Maintains all original video, audio, and subtitle tracks during the transcoding process.
- **Metadata Retention**: Ensures the original file's title is preserved in the output file's metadata.
- **Resource Management**: Monitors and manages system resources to prevent overloading the host computer.
- **Concurrency Control**: Implements a mechanism to prevent duplicate processing of the same file across multiple machines.

## System Requirements

- macOS Sonoma (macOS 14) running on Apple Silicon Macs.
- `ffmpeg` and `ffprobe` installed and accessible in the system's PATH.
- Python 3.8 or newer.

## Installation

1. Clone this repository to your local machine:
   ```shell
   git clone https://github.com/yourusername/yourprojectname.git
2. Ensure `ffmpeg` and `ffprobe` are installed:
   ```bash
   brew install ffmpeg
3. Install required Python dependencies:
   ```bash
   pip install -r requirements.txt

## Contributing

Contributions to improve the transcoding system are welcome. Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- Thanks to the [ffmpeg team](https://ffmpeg.org/) for their incredible tool.
- [Your Name] for project initiation and development.
