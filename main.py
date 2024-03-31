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
import textwrap
from TP_lib import gt1151
from TP_lib import epd2in13_V4 as epd2in13
import time
import logging
from PIL import Image, ImageDraw, ImageFont
import threading
import os

# Initialize e-ink display
epd = epd2in13.EPD()
gt = gt1151.GT1151()
GT_Dev = gt1151.GT_Development()
GT_Old = gt1151.GT_Development()

logging.basicConfig(level=logging.DEBUG)
flag_t = 1

def pthread_irq():
    print("pthread running")
    while flag_t == 1:
        if gt.digital_read(gt.INT) == 0:
            GT_Dev.Touch = 1
        else:
            GT_Dev.Touch = 0
    print("thread:exit")

def update_display(verse_text):
    try:
        print("Updating display...")
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)
        
        # Initialize image
        image = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(image)
        
        # Set font and text color
        font_size = 20
        text_color = 0  # Black
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', font_size)
        
        # Wrap text and draw on the image
        wrapped_text = textwrap.fill(verse_text, width=25)
        draw.text((10, 10), wrapped_text, font=font, fill=text_color)
        
        # Display the image on the e-ink display
        epd.display(epd.getbuffer(image))

        print("Display updated successfully:", verse_text)

    except Exception as e:
        print("Error updating display:", e)

def get_verse():
    # Define a collection of Bible verses
    verses = [
        "For God so loved the world, that he gave his only Son, that whoever believes in him should not perish but have eternal life. - John 3:16",
        "I am the way, and the truth, and the life. No one comes to the Father except through me. - John 14:6",
        "I am the light of the world. Whoever follows me will not walk in darkness, but will have the light of life. - John 8:12",
        "Come to me, all who labor and are heavy laden, and I will give you rest. - Matthew 11:28",
        "For I know the plans I have for you, declares the Lord, plans for welfare and not for evil, to give you a future and a hope. - Jeremiah 29:11",
        "But seek first the kingdom of God and his righteousness, and all these things will be added to you. - Matthew 6:33",
        "Trust in the Lord with all your heart, and do not lean on your own understanding. - Proverbs 3:5",
        "And we know that for those who love God all things work together for good, for those who are called according to his purpose. - Romans 8:28",
        "The Lord is my shepherd; I shall not want. - Psalm 23:1",
        "But they who wait for the Lord shall renew their strength; they shall mount up with wings like eagles; they shall run and not be weary; they shall walk and not faint. - Isaiah 40:31",
        # Add more verses as needed
    ]

    # Return a verse based on the current time (for demonstration purposes)
    current_hour = datetime.now().hour
    verse_index = current_hour % len(verses)
    return verses[verse_index]

if __name__ == "__main__":
    while True:
        verse_text = get_verse()
        
        print("Verse:", verse_text)

        update_display(verse_text)

        # Wait for 2 minutes before updating with the next verse
        print("Waiting for 2 minutes before updating with the next verse...")
        time.sleep(120)  # Sleep for 2 minutes (120 seconds)
