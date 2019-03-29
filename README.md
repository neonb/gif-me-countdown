# gif-me-countdown

Create a minute-long countdown gif.

## Usage

Make sure you have the Pillow library installed:

`pip3 install Pillow`

Put a TrueType font in the repository root directory as `font.ttf`.

Run the script with the countdown target time as a parameter:

`python3 gif.py "2019-03-30T15:00"`

The time format is `%Y-%m-%dT%H:%M`, or `YYYY-MM-DDTHH:MM`. The script works in all UTC.

## Configuration

Copy `default_config.py` to `config.py` to override the default configuration.

Copy `default_end.png` to `end.png` to override the default image used for drawing the ends of the background. The height of the image should match your `IMAGE_HEIGHT` variable. Only the alpha channel is used – it will be colored in according to your `BACKGROUND_COLOR` variable.
