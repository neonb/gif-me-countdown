import sys
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# import and open configuration and resources
try:
    import config
except ImportError:
    import default_config as config

try:
    end = Image.open("end.png")
except FileNotFoundError:
    end = Image.open("default_end.png")

number_font = ImageFont.truetype("font.ttf", 72)
text_font = ImageFont.truetype("font.ttf", 32)

END_WIDTH = config.IMAGE_HEIGHT // 2

def parse_time(time_string):
    return datetime.strptime(time_string, "%Y-%m-%dT%H:%M")

def get_seconds_until(target_time):
    return (target_time - datetime.utcnow()).total_seconds()

background = Image.new("RGB", (config.IMAGE_WIDTH, config.IMAGE_HEIGHT), config.CANVAS_COLOR)
draw = ImageDraw.Draw(background)

# draw background ends
draw.bitmap((0, 0), end, config.BACKGROUND_COLOR)
end = end.transpose(Image.FLIP_LEFT_RIGHT)
draw.bitmap((config.IMAGE_WIDTH - END_WIDTH, 0), end, config.BACKGROUND_COLOR)

# draw background middle part
draw.rectangle((END_WIDTH, 0, config.IMAGE_WIDTH - END_WIDTH, config.IMAGE_HEIGHT), config.BACKGROUND_COLOR)

# draw static numbers of timer
if len(sys.argv) >= 2:
    target_time_string = sys.argv[1]
    delta_seconds = get_seconds_until(parse_time(target_time_string))
else:
    delta_seconds = 43140  # 11 h 59 min

hours = str(int(delta_seconds // 3600)).zfill(2)
minutes = str(int((delta_seconds % 3600) // 60)).zfill(2)
hours_x = END_WIDTH + config.HORIZONTAL_PADDING - number_font.getsize(hours)[0] / 2
draw.text((hours_x, config.NUMBERS_Y), hours, config.TEXT_COLOR, number_font)
minutes_x = config.IMAGE_WIDTH / 2 - number_font.getsize(minutes)[0] / 2
draw.text((minutes_x, config.NUMBERS_Y), minutes, config.TEXT_COLOR, number_font)

# draw static text
hours_text_x = END_WIDTH + config.HORIZONTAL_PADDING - text_font.getsize(config.HOURS_TEXT)[0] / 2
draw.text((hours_text_x, config.TEXT_Y), config.HOURS_TEXT, config.TEXT_COLOR, text_font)
minutes_text_x = config.IMAGE_WIDTH / 2 - text_font.getsize(config.MINUTES_TEXT)[0] / 2
draw.text((minutes_text_x, config.TEXT_Y), config.MINUTES_TEXT, config.TEXT_COLOR, text_font)
seconds_text_x = config.IMAGE_WIDTH - END_WIDTH - config.HORIZONTAL_PADDING - text_font.getsize(config.SECONDS_TEXT)[0] / 2
draw.text((seconds_text_x, config.TEXT_Y), config.SECONDS_TEXT, config.TEXT_COLOR, text_font)

# make first frame
first_frame = background.copy()
draw = ImageDraw.Draw(first_frame)
seconds_x = config.IMAGE_WIDTH - END_WIDTH - config.HORIZONTAL_PADDING - number_font.getsize("59")[0] / 2
draw.text((seconds_x, config.NUMBERS_Y), "59", config.TEXT_COLOR, number_font)
first_frame = first_frame.quantize(config.PALETTE_SIZE)

# other 59 frames
other_frames = []
for i in range(59):
    seconds = str(58 - i).zfill(2)
    frame = background.copy()
    draw = ImageDraw.Draw(frame)
    # just use the horizontal position we calculated for the first frame
    draw.text((seconds_x, config.NUMBERS_Y), seconds, config.TEXT_COLOR, number_font)
    frame = frame.quantize(palette=first_frame)
    other_frames.append(frame)

first_frame.save(
    "out.gif",
    "GIF",
    save_all=True,
    append_images=other_frames,
    disposal=1,
    palette=first_frame.getpalette(),
    optimize=True,
    duration=1000,
    loop=0)
