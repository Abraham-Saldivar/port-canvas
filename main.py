# from datetime import datetime, timedelta
# import requests
# import textwrap
# from flask import Flask, request
# from TP_lib import gt1151
# from TP_lib import epd2in13_V4 as epd2in13
# import time
# import logging
# from PIL import Image, ImageDraw, ImageFont
# import threading
# import subprocess
# import os

# app = Flask(__name__)

# # Canvas API configuration
# CANVAS_API_URL = 'https://canvas.uh.edu/api/v1'
# ACCESS_TOKEN = '23057~o8gIcEuxleDiH3vOQCQT2AxWZlceuIdRusglN94Rf1VC7X83PD3K3ppYGIGiMlay'

# # Initialize e-ink display
# epd = epd2in13.EPD()
# gt = gt1151.GT1151()
# GT_Dev = gt1151.GT_Development()
# GT_Old = gt1151.GT_Development()

# logging.basicConfig(level=logging.DEBUG)
# flag_t = 1

# def pthread_irq():
#     print("pthread running")
#     while flag_t == 1:
#         if gt.digital_read(gt.INT) == 0:
#             GT_Dev.Touch = 1
#         else:
#             GT_Dev.Touch = 0
#     print("thread:exit")

# def update_display(message, page_num, max_pages):
#     try:
#         print("Updating display...")
#         epd.init(epd.FULL_UPDATE)
#         epd.Clear(0xFF)
        
#         # Initialize image
#         image = Image.new('1', (epd.height, epd.width), 255)
#         draw = ImageDraw.Draw(image)
        
#         # Set font and text color
#         font_size = 10
#         text_color = 0  # Black
#         font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', font_size)
        
#         # Wrap text and draw on the image
#         wrapped_text = textwrap.fill(message, width=25)
#         draw.text((10, 10), wrapped_text, font=font, fill=text_color)
        
#         # Add arrow symbol at the bottom right corner
#         arrow = [
#             "     *",
#             "    **",
#             "   ***",
#             "  ****",
#             " *****",
#             "******"
#         ]
#         arrow_height = len(arrow)
#         arrow_width = len(arrow[0])
        
#         for i, line in enumerate(arrow):
#             draw.text((epd.width - arrow_width * 8, epd.height - arrow_height * 15 + i * 15), line, font=font, fill=text_color)
        
#         # Display current page and max pages
#         page_text = f"Page {page_num} of {max_pages}"
#         draw.text((10, epd.height - arrow_height * 15), page_text, font=font, fill=text_color)
        
#         # Display the image on the e-ink display
#         epd.display(epd.getbuffer(image))

#         print("Display updated successfully:", message)

#     except Exception as e:
#         print("Error updating display:", e)

# def get_todo_items():
#     headers = {
#         'Authorization': f'Bearer {ACCESS_TOKEN}',
#     }

#     print("Fetching to-do items from Canvas API...")
#     # Fetch the list of to-do items
#     response = requests.get(
#         f'{CANVAS_API_URL}/users/self/todo', headers=headers)

#     if response.status_code == 200:
#         todo_items = response.json()
#         print("Fetched to-do items:", todo_items)
#         return todo_items
#     else: 
#         print("Failed to fetch to-do items")
#         return []

# def create_todo_items_text(todo_items, page_num, max_items_per_page):
#     start_index = (page_num - 1) * max_items_per_page
#     end_index = start_index + max_items_per_page
#     current_page_items = todo_items[start_index:end_index]
    
#     todo_items_text = ''
    
#     if current_page_items:
#         todo_items_text += 'To-Do Items:\n\n'

#         for item in current_page_items:
#             class_name = item['assignment'].get('course', {}).get('name', 'Unknown Course')
#             assignment_name = item['assignment'].get('name', 'Unknown Assignment')
#             due_date_str = item['assignment'].get('due_at', '')
#             due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M:%SZ') if due_date_str else None
#             formatted_due_date = due_date.strftime('%m/%d/%Y') if due_date else 'Unknown Date'
            
#             item_text = f"* {class_name} - {assignment_name} (Due: {formatted_due_date})\n"
#             todo_items_text += item_text
#     else:
#         print("No to-do items available.")
#         todo_items_text = "No to-do items available."
        
#     print("To-do items text:", todo_items_text)
#     return todo_items_text


# if __name__ == "__main__":
#     max_items_per_page = 2
#     page_num = 1
    
#     while True:
#         todo_items = get_todo_items()
        
#         print("To-do items:", todo_items)

#         max_pages = (len(todo_items) + max_items_per_page - 1) // max_items_per_page
        
#         todo_items_text = create_todo_items_text(todo_items, page_num, max_items_per_page)
        
#         print("To-do items text:", todo_items_text)

#         if todo_items_text:
#             update_display(todo_items_text, page_num, max_pages)
#         else:
#             update_display("No to-do items available.", page_num, max_pages)

#         # Wait for 2 minutes before checking again
#         print("Waiting for 2 minutes before checking again...")
#         time.sleep(300)  # Sleep for 2 minutes (300 seconds)
from datetime import datetime, timedelta
from TP_lib import gt1151
from TP_lib import epd2in13_V4 as epd2in13
from PIL import Image, ImageDraw, ImageFont
import textwrap
import time
import threading

# List of Bible verses
verses = [
    "In the beginning, God created the heavens and the earth. - Genesis 1:1",
    "The earth was without form and void, and darkness was over the face of the deep. And the Spirit of God was hovering over the face of the waters. - Genesis 1:2",
    "And God said, 'Let there be light,' and there was light. - Genesis 1:3",
    "And God saw that the light was good. And God separated the light from the darkness. - Genesis 1:4",
    "God called the light Day, and the darkness he called Night. And there was evening and there was morning, the first day. - Genesis 1:5",
    "And God said, 'Let there be an expanse in the midst of the waters, and let it separate the waters from the waters.' - Genesis 1:6",
    "And God made the expanse and separated the waters that were under the expanse from the waters that were above the expanse. And it was so. - Genesis 1:7",
    "And God called the expanse Heaven. And there was evening and there was morning, the second day. - Genesis 1:8",
    "And God said, 'Let the waters under the heavens be gathered together into one place, and let the dry land appear.' And it was so. - Genesis 1:9",
    "God called the dry land Earth, and the waters that were gathered together he called Seas. And God saw that it was good. - Genesis 1:10",
    "And God said, 'Let the earth sprout vegetation, plants yielding seed, and fruit trees bearing fruit in which is their seed, each according to its kind, on the earth.' And it was so. - Genesis 1:11",
    "The earth brought forth vegetation, plants yielding seed according to their own kinds, and trees bearing fruit in which is their seed, each according to its kind. And God saw that it was good. - Genesis 1:12",
    "And there was evening and there was morning, the third day. - Genesis 1:13",
    "And God said, 'Let there be lights in the expanse of the heavens to separate the day from the night. And let them be for signs and for seasons, and for days and years, - Genesis 1:14",
    "and let them be lights in the expanse of the heavens to give light upon the earth.' And it was so. - Genesis 1:15",
    "And God made the two great lights—the greater light to rule the day and the lesser light to rule the night—and the stars. - Genesis 1:16",
    "And God set them in the expanse of the heavens to give light on the earth, - Genesis 1:17",
    "to rule over the day and over the night, and to separate the light from the darkness. And God saw that it was good. - Genesis 1:18",
    "And there was evening and there was morning, the fourth day. - Genesis 1:19",
    "And God said, 'Let the waters swarm with swarms of living creatures, and let birds fly above the earth across the expanse of the heavens.' - Genesis 1:20",
    "So God created the great sea creatures and every living creature that moves, with which the waters swarm, according to their kinds, and every winged bird according to its kind. And God saw that it was good. - Genesis 1:21",
    "And God blessed them, saying, 'Be fruitful and multiply and fill the waters in the seas, and let birds multiply on the earth.' - Genesis 1:22",
    "And there was evening and there was morning, the fifth day. - Genesis 1:23",
    "And God said, 'Let the earth bring forth living creatures according to their kinds—livestock and creeping things and beasts of the earth according to their kinds.' And it was so. - Genesis 1:24",
    "And God made the beasts of the earth according to their kinds and the livestock according to their kinds, and everything that creeps on the ground according to its kind. And God saw that it was good. - Genesis 1:25",
    "Then God said, 'Let us make man in our image, after our likeness. And let them have dominion over the fish of the sea and over the birds of the heavens and over the livestock and over all the earth and over every creeping thing that creeps on the earth.' - Genesis 1:26",
    "So God created man in his own image, in the image of God he created him; male and female he created them. - Genesis 1:27",
    "And God blessed them. And God said to them, 'Be fruitful and multiply and fill the earth and subdue it, and have dominion over the fish of the sea and over the birds of the heavens and over every living thing that moves on the earth.' - Genesis 1:28",
    "And God said, 'Behold, I have given you every plant yielding seed that is on the face of all the earth, and every tree with seed in its fruit. You shall have them for food. - Genesis 1:29",
    "And to every beast of the earth and to every bird of the heavens and to everything that creeps on the earth, everything that has the breath of life, I have given every green plant for food.' And it was so. - Genesis 1:30",
    "And God saw everything that he had made, and behold, it was very good. And there was evening and there was morning, the sixth day. - Genesis 1:31",
    "Thus the heavens and the earth were finished, and all the host of them. - Genesis 2:1",
    "And on the seventh day God finished his work that he had done, and he rested on the seventh day from all his work that he had done. - Genesis 2:2",
    "So God blessed the seventh day and made it holy, because on it God rested from all his work that he had done in creation. - Genesis 2:3",
    "These are the generations of the heavens and the earth when they were created, in the day that the LORD God made the earth and the heavens. - Genesis 2:4",
    "When no bush of the field was yet in the land and no small plant of the field had yet sprung up—for the LORD God had not caused it to rain on the land, and there was no man to work the ground, - Genesis 2:5",
    "and a mist was going up from the land and was watering the whole face of the ground— - Genesis 2:6",
    "then the LORD God formed the man of dust from the ground and breathed into his nostrils the breath of life, and the man became a living creature. - Genesis 2:7",
    "And the LORD God planted a garden in Eden, in the east, and there he put the man whom he had formed. - Genesis 2:8",
    "And out of the ground the LORD God made to spring up every tree that is pleasant to the sight and good for food. The tree of life was in the midst of the garden, and the tree of the knowledge of good and evil. - Genesis 2:9",
    "A river flowed out of Eden to water the garden, and there it divided and became four rivers. - Genesis 2:10",
    "The name of the first is the Pishon. It is the one that flowed around the whole land of Havilah, where there is gold. - Genesis 2:11",
    "And the gold of that land is good; bdellium and onyx stone are there. - Genesis 2:12",
    "The name of the second river is the Gihon. It is the one that flowed around the whole land of Cush. - Genesis 2:13",
    "And the name of the third river is the Tigris, which flows east of Assyria. And the fourth river is the Euphrates. - Genesis 2:14",
    "The LORD God took the man and put him in the garden of Eden to work it and keep it. - Genesis 2:15",
    "And the LORD God commanded the man, saying, 'You may surely eat of every tree of the garden, - Genesis 2:16"
]



# Initialize e-ink display
epd = epd2in13.EPD()
gt = gt1151.GT1151()
GT_Dev = gt1151.GT_Development()
GT_Old = gt1151.GT_Development()

# Function to update display with the next verse
def update_display():
    try:
        print("Updating display...")
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)
        
        # Initialize image
        image = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(image)
        
        # Set font and text color
        font_size = 12
        text_color = 0  # Black
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', font_size)
        
        # Get the next verse
        global current_verse_index
        current_verse_index = (current_verse_index + 1) % len(verses)
        current_verse = verses[current_verse_index]
        
        # Wrap text and draw on the image
        wrapped_text = textwrap.fill(current_verse, width=25)
        draw.text((10, 10), wrapped_text, font=font, fill=text_color)
        
        # Display the image on the e-ink display
        epd.display(epd.getbuffer(image))

        print("Display updated successfully with verse:", current_verse)

    except Exception as e:
        print("Error updating display:", e)

# Timer function to update display every 120 seconds
def timer_thread():
    while True:
        update_display()
        time.sleep(30)  # Sleep for 120 seconds (2 minutes)

# Initialize verse index
current_verse_index = -1

# Start timer thread
timer_thread = threading.Thread(target=timer_thread)
timer_thread.daemon = True
timer_thread.start()

# Keep main thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
