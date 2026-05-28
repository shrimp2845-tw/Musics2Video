
## About

- **Author:** shrimp2845  
- **Version:** 0.2.0
- **requirement**: Python 3.10+, FFmpeg
- **License:** MIT

**Musics2Video** is a Python CLI tool for automatically generating music playlist videos. It can fetch music from online sources like YouTube or use your local audio files, combine them with a dynamic playlist display, and render a single video file.

## Features

**Flexible Music Sources:** Create videos from a list of online URLs (`yt-dlp` supported sources) or local audio files.

**Batch Processing:** Use a simple text file to define a mixed playlist of online and local tracks.

**Customizable Visuals:**
Choose from built-in styles (`classic`,`modern`) or create and use your own custom HTML/CSS templates for a unique look.

**Automatic Metadata:** Automatically fetches song titles and thumbnails from online sources.

**Custom Artwork:** Specify unique cover art for each track in your playlist.

**Configurable Output:** Control video resolution, FPS, audio quality, and output formats.

## Installation
 **FFmpeg**: This tool relies on FFmpeg for video and audio processing. You can download it from the [official FFmpeg website](https://ffmpeg.org/download.html).

 **Musics2Video**: Install the package using `pip`.

Python 3.10 ~ 3.12
```sh
pip install musics2video
```
Python 3.13+
```sh
pip install musics2video
pip install audioop-lts
```


## Usage

The tool is accessed using `musics2video` command, which has two main  sub-commands: `download` and `list`.

### 1. `download` Command

Generates a video from a list of online URLs. Audio is downloaded, and titles/thumbnails are fetched automatically.

**Example:**
```sh
musics2video download "https://www.youtube.com/watch?v=xxxxxx" "https://www.youtube.com/watch?v=yyyyyy" --name "my_playlist.mp4" --style modern
```

### 2. `list` Command

Generates a video from a text file that specifies a sequence of local and online tracks. This method provides fine-grained control over the playlist content and artwork.

**List File Format:**
Create a text file (e.g., `songs.txt`). Each line represents a track and follows this format:
`source{{NEXT}}path_or_url{{NEXT}}optional_cover_path`

*   `source`: Can be `local` or `download`.
*   `path_or_url`: A file path for `local` or a URL for `download`.
*   `optional_cover_path`: An optional path to a local image file to use as the track's cover art.

**Example `songs.txt`:**
```
download{{NEXT}}https://www.youtube.com/watch?v=xxxxxx
local{{NEXT}}/path/to/my/song.mp3{{NEXT}}/path/to/my/album_art.png
download{{NEXT}}https://www.youtube.com/watch?v=yyyyyy{{NEXT}}/path/to/custom_cover.jpg
local{{NEXT}}/another/path/to/music.wav
```

**Command:**
```sh
musics2video list songs.txt --name "my_mixed_playlist.mp4" --style classic
```

### Command-line Options

Both `download` and `list` commands accept the following options to customize the output:

| Option                           | Alias | Description                                                           | Default          |
|----------------------------------|-------|-----------------------------------------------------------------------|------------------|
| `--name`                         | `-n`  | The filename for the final output video.                              | `output.mp4`     |
| `--out-dir`                      | `-o`  | Target output directory path for the final video.                     | `./`             |
| `--style`                        | `-s`  | Built-in visual style template (`classic`, `modern`).                 | `classic`        |
| `--custom-tmpl`                  |       | Path to a folder containing a custom `template.html` and `style.css`. | `None`           |
| `--width`                        |       | Output video resolution width in pixels.                              | `1920`           |
| `--height`                       |       | Output video resolution height in pixels.                             | `1080`           |
| `--fps`                          |       | Frames per second for the final video.                                | `10`             |
| `--yt-cover` / `--no-yt-cover`   |       | Fetch and use thumbnails from online video sources.                   | `--yt-cover`     |
| `--shorten` / `--no-shorten`     |       | Truncate long track titles to fit the layout.                         | `--shorten`      |
| `--audio-fmt`                    |       | Target audio format for internal processing.                          | `opus`           |
| `--audio-q`                      |       | Audio extraction quality (0=best, 9=worst).                           | `0`              |
| `--video-fmt`                    |       | Output video file container format.                                   | `mp4`            |
| `--level`                        | `-l`  | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`).                  | `INFO`           |
| `--keep-temp`/`--no-keep-temp`   |       | whether to remove temporary files or not                              | `--no-keep-temp` |

## Built-in templates display

Two Built-in templates provided in current version:

### 1.classic
![classic](https://raw.githubusercontent.com/shrimp2845-tw/Musics2Video/refs/heads/main/images/classic.gif)

### 2.modern
![modern](https://raw.githubusercontent.com/shrimp2845-tw/Musics2Video/refs/heads/main/images/modern.gif)

(These songs are pretty good! You should take a look at their [official website](https://milpr.com/))

## Custom Templates

If you don't like buit-in templates, you can provide your own template directory using the `--custom-tmpl` option. The directory must contain:

1.`template.html`: The HTML structure for your video frame.

2.`style.css`: The CSS for styling the frame.

### Template Requirements

 **`template.html`**:

It must contain the `{{SONGS}}` placeholder. `musics2video` will replace this with the generated HTML for the song list.

It should reference a cover image. The generator places an image named `cover.png` in the rendering directory. You can reference it in your HTML like this: `<img src="cover.png">`.

**`style.css`**:

The playlist generated at `{{SONGS}}` will consist of `<div class="song">...</div>` elements.

The currently playing song will have an additional class: `<div class="song active">...</div>`. You can use `.song.active` to highlight it.

**Example Custom Template Structure:**
```
/my_project
├── my_template/
│   ├── template.html
│   └── style.css
└── songs.txt
```

**Command:**
```sh
musics2video list songs.txt --custom-tmpl ./my_template
```

## Disclaimer 

If you want to redistribute the videos generated by this tool, please **make sure to obtain permission from the original author**. The author of this project takes no responsibility if you run into any issues.

## Note

This project is maintained by a beginner.  
Any feedback, suggestions, issues are very welcome!