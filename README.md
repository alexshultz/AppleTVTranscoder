# Video Transcoding System targeted at Plex serving videos for AppleTV

This project provides a comprehensive solution for transcoding video files format, optimized for playback on Apple devices, focusing on AppleTV. It leverages the efficiency of H.264 and H.265 to reduce file sizes while maintaining high video quality. The system is designed to run on a network of Apple Silicon Macs, using CPU and hardware processing for video files stored on a NAS.

## Features

- **Dynamic Resolution Handling**: Converts and downscales 4K videos to 1080p, 720p and 480p, adjusting resolution based on the original video.
- **Track Preservation**: Keeps main video stream, and English audio and subtitle streams during the transcoding process.
- **Metadata Retention**: Adds original filename and video encoding settings as comments to the file.
- **Resource Management**: Monitors and manages system resources to prevent overloading the host computer storage space.
- **Concurrency Control**: Implements a mechanism to prevent duplicate processing of the same file across multiple machines.

## System Requirements

- macOS Sonoma (macOS 14) running on Apple Silicon Macs. Probably will work on other versions but not tested.
- `exiftool`, `ffmpeg` and `ffprobe` installed and accessible in the system's PATH.
- Python 3.8 or newer.

## Installation

1. Clone this repository to your local machine:
   ```shell
   git clone https://github.com/alexshultz/https://github.com/alexshultz/AppleTVTranscoder.git
1. Ensure `exiftool` is installed:
   ```bash
   brew install exiftool
1. Ensure `ffmpeg` and `ffprobe` are installed:
   ```bash
   brew install ffmpeg
1. Install required Python dependencies:
   ```bash
   pip install -r requirements.txt

## Contributing

Contributions to improve the transcoding system are welcome. Please follow these steps to contribute:

1. Fork the repository.
1. Create a new branch for your feature (`git checkout -b feature/AmazingFeature`).
1. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
1. Push to the branch (`git push origin feature/AmazingFeature`).
1. Open a pull request.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- Thanks to the [exiftool team] (https://exiftool.org) and the [ffmpeg team](https://ffmpeg.org/) for their incredible tool.
- Thanks to several AI groups, including `ChatGPT`, `Gemini`, and `GitHub Copilot` for creating great help to get me started on this project.


# Video Encoding Strategy

## Overview

This document outlines the video encoding strategy designed to serve high-quality video content across a range of devices, with special attention to compatibility with Apple silicon and hardware. The goal is to create encoded files ready for streaming via Plex without necessitating any real-time processing or transcoding, ensuring an optimal viewing experience across all network conditions.

## Encoding Goals

- **Compatibility**: Ensure broad support across Apple devices by using widely supported codecs.
- **Quality Preservation**: Maintain the best possible visual quality, with considerations for both HDR and SDR content.
- **Efficiency**: Optimize file sizes to balance quality with streaming and storage requirements.
- **Adaptive Streaming**: Provide multiple resolution options to suit different devices and network speeds.

## Encoding Rules by Resolution

### 4K HDR

- **Video Streams**: Use H.265 (HEVC) for efficient compression that retains HDR details. Use hardware encoding for speed. Apply a high quality setting for a balance between encode time, output quality, and file size, with a Q of 75 for high-quality compression.
  - **Sample Command**:
    ```
    -c:v hevc_videotoolbox -q:v 75 -tag:v hvc1
    ```

- **Audio Streams**: Encode original non-AAC English audio streams to AAC.
  - **Sample Command**:
    ```
    -c:a aac -b:a 768k -ar 48000 -ac 6 -metadata:s:a language=eng
    ```

- **Subtitle Streams**: Keep English subtitle streams. Encode a `mov_text` version for internal subtitles and provide external SRT versions, as well.
  - **Sample Command for internal subtitle streams**:
    ```
    -c:s mov_text -metadata:s:s language=eng
    ```

  - **Sample Command for external subtitle streams**:
    ```
    -c:s copy external_file.srt
    ```


### 1080p SDR (from HDR Source)

- **Video Streams**:
  - **Codec**: Use H.265 (HEVC) for efficient compression.
  - **Resolution**: Downscale to 1080p to cater to devices and networks that cannot support 4K streaming.
  - **Tone Mapping**: Implement HDR to SDR conversion via tonemapping to ensure visual quality on SDR displays.
  - **Compression**: Apply a high quality setting for a balance between encode time, output quality, and file size, with a Q of 75 for high-quality compression.
  - **Sample Command**:
    ```
    -c:v hevc_videotoolbox -q:v 75 -tag:v hvc1 "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,scale=1920x1080
    ```

- **Audio Streams**:
  - **Codec**: Encode original non-AAC English audio streams to AAC.
  - **Additional Streams**: If a stereo stream is not provided, add a stereo downscale stream.
  - **Sample Command for Original Stream**:
    ```
    -c:a aac -b:a 768k -ar 48000 -ac 6 -metadata:s:a language=eng
    ```
  - **Sample Command for Downscale Stream**:
    ```
    -c:a aac -b:a 128k -ar 48000 -ac 2 -metadata:s:a language=eng
    ```
    
- **Subtitle Streams**: Keep English subtitle streams. Encode a `mov_text` version for internal subtitles and provide external SRT versions, as well.
  - **Sample Command for internal subtitle streams**:
    ```
    -c:s mov_text -metadata:s:s language=eng
    ```

  - **Sample Command for external subtitle streams**:
    ```
    -c:s copy external_file.srt
    ```

### 720p SDR

- **Objective**: Provide suitable video stream for less-capable devices as well as for devices that default to 720p streams.

- **Video Streams**:
  - **Codec**: H.264 (AVC) to ensure compatibility with older or less capable devices.
  - **Resolution**: Downscale to 720p, suitable for many default video player setups.
  - **Tone Mapping**: Implement HDR to SDR conversion via tonemapping to ensure visual quality on SDR displays.
  - **Compression**: Apply a high quality setting for a balance between encode time, output quality, and file size, with a Q of 75 for high-quality compression.
  - **Sample Command**:
    ```
    -c:v h264_videotoolbox -q:v 75  "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,scale=-2:720"
    ```

- **Audio Streams**:
  - **Codec**: Encode original non-AAC English audio streams to AAC.
  - **Additional Streams**: If a stereo stream is not provided, add a stereo downscale stream.
  - **Sample Command for Original Stream**:
    ```
    -c:a aac -b:a 768k -ar 48000 -ac 6 -metadata:s:a language=eng
    ```
  - **Sample Command for Downscale Stream**:
    ```
    -c:a aac -b:a 128k -ar 48000 -ac 2 -metadata:s:a language=eng
    ```

- **Subtitle Streams**: Keep English subtitle streams. Encode a `mov_text` version for internal subtitles and provide external SRT versions, as well.
  - **Sample Command for internal subtitle streams**:
    ```
    -c:s mov_text -metadata:s:s language=eng
    ```

  - **Sample Command for external subtitle streams**:
    ```
    -c:s copy external_file.srt
    ```

### 480p SDR (for Mobile Data)

- **Objective**: Maximize compression to facilitate streaming over mobile data while preserving watchable quality.

- **Video Streams**:
  - **Codec**: H.264 (AVC) to ensure compatibility with older or less capable devices.
  - **Resolution**: Scale down to 480p, ideal for mobile devices or constrained bandwidth scenarios.
  - **Tone Mapping**: Implement HDR to SDR conversion via tonemapping to ensure visual quality on SDR displays.
  - **Compression**: Apply a high quality setting for a balance between encode time, output quality, and file size, with a Q of 75 for high-quality compression.
  - **Sample Command**:
    ```
    -c:v h264_videotoolbox -q:v 75  "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,scale=-2:480"
    ```

- **Audio Streams**:
  - **Codec**: Encode original non-AAC English audio streams to AAC as stereo (or mono).

  - **Sample Command for Downscale Stream**:
    ```
    -c:a aac -b:a 128k -ar 48000 -ac 2 -metadata:s:a language=eng
    ```

- **Subtitle Streams**: Keep English subtitle streams. Encode a `mov_text` version for internal subtitles and provide external SRT versions, as well.
  - **Sample Command for internal subtitle streams**:
    ```
    -c:s mov_text -metadata:s:s language=eng
    ```

  - **Sample Command for external subtitle streams**:
    ```
    -c:s copy external_file.srt
    ```

## Additional Considerations

- **Audio Encoding**: Align audio stream encoding standards to complement video quality across all resolutions. Ensure that audio encoding is compatible with target devices and does not require real-time processing or transcoding by the server.
  
- **Device Testing**: Validate encoded content across a spectrum of devices to ensure compatibility and user satisfaction. This includes testing on various Apple devices to confirm that no extra processing is needed for playback.

- **Plex Configuration**: Check Plex server settings to optimize file delivery based on the client device's capabilities and current network conditions. Ensure that Plex is set up to serve the correct file version directly, avoiding any on-the-fly transcoding that could strain the server or degrade the viewing experience.

## Conclusion

Adhering to these video encoding guidelines ensures that your content is prepared with the highest quality and efficiency in mind, tailored for streaming across a variety of devices and network conditions. By providing multiple resolutions and optimizing for both HDR and SDR, viewers can enjoy the best possible experience tailored to their specific device and connection. This strategy aims to streamline your Plex media server's operation, ensuring smooth playback without the need for additional processing, thus enhancing the overall user experience.

# Audio Encoding Strategy

## Overview

The primary goal of this audio encoding strategy is to ensure that audio tracks extracted from TV shows, movies, and podcasts are encoded in a way that balances audio quality with file size efficiency. The strategy differentiates between "large" files, where the preservation of original audio quality is paramount, and "smaller" files, where file size efficiency and compatibility take precedence.

## Encoding Goals

- **Compatibility**: Ensure broad support across Apple devices by using widely supported codecs.
- **Quality Preservation**: Maintain the best possible audio quality, with considerations for both high-quality sound systems (5.1) and less-capable sound systems (stereo, mono).
- **Efficiency**: Optimize file sizes to balance quality with streaming and storage requirements.
- **Adaptive Streaming**: Provide multiple resolution options to suit different devices and network speeds.

## Encoding Rules by Resolution

### For Large Files (4k, 1080p, 720p)

- **Objectives** Preserve high audio quality similar to the original by maintaining the original bitrate, channel configuration, and sample rate.
- **Audio Streams**:
  - **Codec**: Encode original non-AAC English audio streams to AAC.
  - **Bit Rate**: Maintaining the original bit rate.
  - **Sample Rate**: Maintaining the original sample rate.
  - **Channel Configuration**: Maintaining the original channel configuration. Add a stereo downscale stream for users with less capable audio systems, if one does not exist.
  - **Sample Command for Original Stream**:
    ```
    -c:a aac -b:a 768k -ar 48000 -ac 6 -metadata:s:a language=eng
    ```
  - **Sample Command for Downscale Stream**:
    ```
    -c:a aac -q:a 5 -ac 2 -metadata:s:a language=eng
    ```

### For Smaller Files

- **Objectives** Optimize for smaller file size without significantly compromising audio quality, targeting more efficient bandwidth use and storage.
- **Downsample audio channels** to stereo or mono, depending on the original channel layout, to achieve compatibility across a wide range of playback devices.

- **Audio Streams**:
  - **Codec**: Encode original non-AAC English audio streams to AAC.
  - **Bit Rate**: Maintaining the original bit rate.
  - **Sample Rate**: Adjust original sample rate to be suitable for stereo, if needed.
  - **Channel Configuration**: Downscale original stream to stereo for users with less capable audio systems, if one does not exist. Keep original stream mono if it already exists.
  - **Sample Command for Downscale Stream**:
    ```
    -c:a aac -q:a 5 -ac 2 -metadata:s:a language=eng
    ```

## Implementation Details

To implement this strategy, a programmer will need to:

1. **Analyze Audio Tracks**: Use `ffprobe` to gather information on the audio stream's codec, bitrate, channel layout, and sample rate.
1. **Define Encoding Parameters**:
   - For large files: Preserve original attributes but use VBR to potentially reduce file size while maintaining quality.
   - For smaller files: Adjust channel layout and VBR settings for efficiency.
1. **Encode with `ffmpeg`**:
   - Always use the AAC codec (`-c:a aac`).
   - Apply VBR with a quality level suitable for the file's designated size category (`-q:a` value).
   - Adjust channel layout (`-ac`) based on file size goals and original content.
   - Apply sample rate (`-ar`) based on file size goals and original content.
   - Use quality-based encoding when needed for smaller file sizes (`-q:a`)


### Example Commands

#### Large Files
```bash
ffmpeg -i input.mkv -c:a aac -q:a 3 -ac <original_channels> -ar <original_sample_rate> output.m4a
```

#### Smaller Files

For smaller files, adjust the channel layout and VBR settings for efficiency:

```bash
ffmpeg -i input.mkv -c:a aac -q:a 5 -ac 2 output.m4a
```

*Note: For smaller files, use `-ac 2` to downmix to stereo if the original content had more than two channels. For mono content, keep it mono with `-ac 1`.*

### Notes for Programmers

- **VBR Quality Levels**: The `-q:a` parameter in `ffmpeg` controls the VBR quality level for AAC. Lower numbers indicate higher quality. For smaller files aimed at reducing file size while maintaining clarity, especially for speech, a `-q:a` setting of 5 is recommended.
  
- **Channel Layout Decision**: It's essential to implement logic that assesses the original number of audio channels. If the source has more than two channels, consider downmixing to stereo for efficiency and broader compatibility. Process mono audio tracks as as mono tracks to prevent unnecessary upmixing.

- **Automation and Scripting**: Develop a script or software that automates this decision-making process. Use `ffprobe` to analyze the audio stream's properties and then apply the corresponding `ffmpeg` encoding parameters. This automation ensures consistency and efficiency, particularly valuable when processing large batches of files.

## Extracting Audio Information

Use `ffprobe` to analyze the video file and identify audio streams.

To analyze audio streams within a video file and extract relevant information such as the stream index, codec name, stream type, and language, you can use the `ffprobe` tool with the following command:

```bash
ffprobe -v error -select_streams a -show_entries stream=index,codec_name,codec_type,sample_rate,channels -show_entries stream_tags=language,bps -of csv=p=0 input.mkv
```

Explanation of the command options:

- `-v error`: Sets the logging level to 'error', which means only error messages will be shown.
- `-select_streams a`: Selects only audio streams for analysis.
- `-show_entries stream=index,codec_name,codec_type`: Specifies the information to output, which includes the stream's index number, codec name, sample rate, and channels.
- `-show_entries stream_tags=language,bps`: Specifies the tag information to output, which includes the stream's tag:language and tag:bps.
- `-of csv=p=0`: Sets the output format to 'csv' (Comma-Separated Values) and the printer parameter to '0' to ensure a simple CSV format without extra information or headers.

This command will produce a CSV-formatted output with each piece of data separated by a comma, providing a clean and parsable list of information about each subtitle stream in the file `input.mkv`.

### Interpreting ffprobe Output

The output from `ffprobe` will look something like this:

```bash
0,eac3,audio,48000,6,eng,768000
1,aac,audio,48000,2,eng,128000
2,ac3,audio,48000,2,spa,128000
```

In this output:

- The first entry is an EAC3 audio stream at 48khz, 6 channels, and 768kbps in English (index 0).
- The second entry is an AAC audio stream at 48khz, 2 channels, 128kbps in English (index 1).
- The third entry is an AC3 audio stream at 48khz, 2 channels, at 128kbps in Spanish (index 2).

### Selecting and Embedding Specific Audio Streams

With this information, construct an `ffmpeg` command to map only English audio streams into the output file:

```bash
ffmpeg -i input.mkv -map 0:v -map 0:a:0 -c copy -c:a aac -b:a 768k -ar 48000 -ac 6 -metadata:s:a language=eng output.mp4
```

In this command:

- `-map 0:v` selects the video stream(s).
- `-map 0:a:0` selects audio stream 0.
- `-c copy` directly copies the selected streams without re-encoding.
-  `-c:a aac -b:a 768k -ar 48000 -ac 6` overrides the direct copy command and encodes audio stream 0 in to AAC format at 768kbps at 48khz with 6 channels. 
- `-metadata:s:a language=eng` tags the audio stream as English. This is crucial for players that use metadata to select default languages for audio.

For more granular control, you can explicitly map each English audio stream if you have their indexes:

```bash
ffmpeg -i input.mkv -map 0:v -map 0:a:0 -map 0:a:1 -c copy -c:a:0 aac -b:a 768k -ar 48000 -ac 6 -metadata:s:a language=eng output.mp4
```
In this command:

- `-map 0:v` selects the video stream(s).
- `-map 0:a:0` selects audio stream 0.
- `-map 0:a:1` selects audio stream 2.
- `-c copy` direct copies mapped streams without re-encoding.
-  `-c:a:0 aac -b:a 768k -ar 48000 -ac 6` overrides the direct copy command and encodes audio stream 0 in to AAC format at 768kbps at 48khz with 6 channels. 
- `-metadata:s:a language=eng` tags all the audio streams as English. This is crucial for players that use metadata to select default languages for audio.

*Note: It is possible to set mapping and metadata by streams. Indexing of each type of stream starts at 0.
Adjust the `-map 0:a:x` and `-metadata:s:a:x language=eng` options according to the actual stream indexes of the audio in your input file. If you wish to set different language options for streams then change `eng` for each stream to the appropriate language.*

*Note: The order of `-map` determines the order that the streams will appear in the output file. Neglecting a `-map` option implicitly maps a single stream of each type in the file, based on the order in which they appear in the original file. It is possible that `ffmpeg` will choose unexpected streams if it is looking for certain types of streams (e.g. certain langauges). *

### Selecting English Audio Streams in ffmpeg

It is possible to construct an `ffmpeg` command to map all, and only, English audio streams into the output file:

```bash
ffmpeg -i input.mkv -map 0:v -map 0:a:m:language:eng -c copy output.mp4
```

In this command:

- `-map 0:v` selects the video stream(s).
- `-map 0:a:m:language:eng` selects all audio streams that are tagged as English. It assumes there are English audio streams. This version: `-map 0:a:m:language:eng?` will gracefully exit ffmpeg if there are none.
- `-c copy` copies the selected streams without re-encoding.

*Note: Use this method when you are sure there are English audio streams and you want to avoid mapping English audio streams individually. You can still copy or encode specific audio streams if you know their index.*

### Conclusion

Adopting these encoding strategies ensures that audio files, whether part of larger high-definition content or destined for mobile and web use, are treated optimally. This approach not only preserves audio quality where necessary but also optimizes for file size and compatibility, striking a balance that meets the needs of varied distribution channels and playback devices. By applying these tailored settings, the encoded audio will provide a satisfactory listening experience, whether it's part of a cinematic sound mix or a simple podcast.

# Subtitle Encoding Strategy Documentation

## Goals

The goal is to identify, convert (if necessary), embed English subtitle streams into MP4 files during the video encoding process, and provide subtitle streams as external files. This ensures all English subtitles are kept and correctly tagged, enhancing accessibility and viewer experience with non-transcoding needed for devices that need `mov_text` or `subrip` style subtitles.

### Rules for Processing English Subtitles

1. **Identify Subtitle Streams**: Utilize `ffprobe` to list all available subtitle streams in the source file, extracting crucial metadata including the language.

1. **Determine English Subtitles**: Filter subtitle streams to identify those tagged with English language codes (`eng` or `en`).

1. **Check Format Compatibility**: Verify the subtitle format is compatible with the MP4 container. Convert subtitles to a compatible format (e.g., SRT to `mov_text`) as needed.

1. **Embed All English Subtitles**: Convert and embed all identified English subtitle streams into the MP4 file, ensuring each stream is correctly tagged with English metadata.

1. **Ignore Non-English Subtitles**: Exclude subtitle streams that are not in English from the conversion and embedding process.

## Implementation Details

To implement this strategy, a programmer will need to:

1. **Analyze Subtitle Tracks**: Use `ffprobe` to gather information on the subtitle stream's codec and language.
1. **Define Encoding Parameters**:
   - Only consider English subtitles
   - Only consider text-based subtitles
1. **Encode with `ffmpeg`**:
   - Always use the mov_text codec (`-c:s mov_text`) for internal files.
   - After setting up processing and output for video/audio/subtitle file, map one external subtitel at a time and copy it to an external `.srt` file. This can be done as one long 'ffmpeg' command where after each file is set up the you map the input file again to get the specific stream you want to output. You can also do this as separate 'ffmpeg' commands.
   - Add language metadata for internal subtitles (`metadata:s:s language=eng`)

## Extracting Subtitle Information

Use `ffprobe` to analyze the video file and identify subtitle streams.

To analyze subtitle streams within a video file and extract relevant information such as the stream index, codec name, stream type, and language, you can use the `ffprobe` tool with the following command:

```bash
ffprobe -v error -select_streams s -show_entries stream=index,codec_name,codec_type -show_entries stream_tags=language -of csv=p=0 input.mkv
```

Explanation of the command options:

- `-v error`: Sets the logging level to 'error', which means only error messages will be shown.
- `-select_streams s`: Selects only subtitle streams for analysis.
- `-show_entries stream=index,codec_name,codec_type`: Specifies the information to output, which includes the stream's index number, codec name, type, and language.
- `-show_entries stream_tags=language`: Specifies the tag information to output, which includes the stream's tag:language.
- `-of csv=p=0`: Sets the output format to 'csv' (Comma-Separated Values) and the printer parameter to '0' to ensure a simple CSV format without extra information or headers.

This command will produce a CSV-formatted output with each piece of data separated by a comma, providing a clean and parsable list of information about each subtitle stream in the file `input.mkv`.

### Interpreting ffprobe Output

The output from `ffprobe` will look something like this:

```bash
0,subrip,subtitle,eng
1,ass,subtitle,eng
2,hdmv_pgs_subtitle,subtitle,spa
```

In this output:

- The first entry is a subrip subtitle stream in English (index 0). This type of stream can be converted to use in mp4 files.
- The second entry is an ass (SSA (SubStation Alpha) subtitle) subtitle stream in English (index 1). This type of stream can be converted to use in mp4 files.
- The third entry is an hdmv_pgs_subtitle (HDMV Presentation Graphic Stream subtitles) subtitle stream in Spanish (index 2). This type of subtitle cannot be directly converted to use in mp4 files. It is an image-based file. It is possible to OCR the information and then create a text-based subtitle but that is not covered here.

### Selecting and Embedding Specific Subtitle Streams

With this information, construct an `ffmpeg` command to map the firsrt English subtitle stream into the output file:

```bash
ffmpeg -i input.mkv -map 0:v -map 0:a -map 0:s:0 -c copy -c:s mov_text -metadata language=eng output.mp4
```

In this command:

- `-map 0:v` selects the video stream(s).
- `-map 0:a` selects the audio stream(s).
- `-map 0:s:0` selects subtitle stream 0
- `-c copy` direct copies the selected streams without re-encoding.
- `-c:s mov_text` converts selected subtitle streams to a format compatible with MP4 containers, necessary for ensuring subtitles are playable on a wide range of devices, including Apple hardware.
- `-metadata language=eng` tags all streams as English. This is crucial for players that use metadata to select default languages for subtitles.

*Note: Use `metadata:s:s language=eng` to set language info for all subtitle files.* 

*Note: It is possible to set mapping and metadata by streams. Indexing of each type of stream starts at 0.
Adjust the `-map 0:s:x` and `-metadata:s:s:x language=eng` options according to the actual stream indexes of the subtitles in your input file. If you wish to set different language options for streams then change `eng` for each stream to the appropriate language.*

*Note: The order of `-map` determines the order that the streams will appear in the output file. Neglecting a `-map` option implicitly maps a single stream of each type in the file, based on the order in which they appear in the original file. It is possible that `ffmpeg` will choose unexpected streams if it is looking for certain types of streams (e.g. certain langauges). *

### Example code to select individual English Subtitle streams.

```
import subprocess
import json

# Specify the path to your input video file
input_file = 'input.mkv'

def get_english_subtitle_streams(input_file):
    """Uses ffprobe to list all English subtitle streams with the updated command."""
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 's',
        '-show_entries', 'stream=index,codec_name,codec_type',
        '-show_entries', 'stream_tags=language',
        '-of', 'json',
        input_file
    ]
    
    # Run the ffprobe command and capture the output
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    streams = json.loads(result.stdout)
    
    # Filter for English subtitles
    eng_sub_indices = [
        stream['index']
        for stream in streams.get('streams', [])
        if stream.get('tags', {}).get('language') == 'eng'
    ]
    
    return eng_sub_indices

def extract_subtitles(input_file, subtitle_indices):
    """Extracts subtitles based on the provided indices, adjusted for the updated command output."""
    for index in subtitle_indices:
        output_file = f"{input_file.rsplit('.', 1)[0]}_subtitles_{index}.srt"
        
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-map', f'0:s:{index}',
            '-c:s', 'srt',
            output_file
        ]
        
        # Run the ffmpeg command to extract subtitles
        subprocess.run(cmd)
        print(f"Extracted subtitle stream {index} to {output_file}")

def main():
    subtitle_indices = get_english_subtitle_streams(input_file)
    if subtitle_indices:
        print(f"Found English subtitles at streams: {subtitle_indices}")
        extract_subtitles(input_file, subtitle_indices)
    else:
        print("No English subtitles found.")

if __name__ == "__main__":
    main()
```

### Conclusion

Adopting these encoding strategies ensures that English subtitle files will be included in the file.