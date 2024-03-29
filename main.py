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

# def update_display(message):
#     try:
#         print("Updating display...")
#         epd.init(epd.FULL_UPDATE)
#         epd.Clear(0xFF)
        
#         # Initialize image
#         image = Image.new('1', (epd.height, epd.width), 255)
#         draw = ImageDraw.Draw(image)
        
#         # Set font and text color
#         font_size = 20
#         text_color = 0  # Black
#         font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', font_size)
        
#         # Wrap text and draw on the image
#         wrapped_text = textwrap.fill(message, width=25)
#         draw.text((10, 10), wrapped_text, font=font, fill=text_color)
        
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

# def create_todo_items_text(todo_items):
#     todo_items_text = ''
    
#     if todo_items:
#         todo_items_text += 'To-Do Items:\n\n'

#         for item in todo_items:
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
#     while True:
#         todo_items = get_todo_items()
        
#         print("To-do items:", todo_items)

#         todo_items_text = create_todo_items_text(todo_items)
        
#         print("To-do items text:", todo_items_text)

#         if todo_items_text:
#             update_display(todo_items_text)
#         else:
#             update_display("No to-do items available.")

#         # Wait for 2 minutes before checking again
#         print("Waiting for 2 minutes before checking again...")
#         time.sleep(300)  # Sleep for 2 minutes (300 seconds)
from datetime import datetime, timedelta
import requests
import textwrap
from flask import Flask, request
from TP_lib import gt1151
from TP_lib import epd2in13_V4 as epd2in13
import time
import logging
from PIL import Image, ImageDraw, ImageFont
import threading
import subprocess
import os

app = Flask(__name__)

# Canvas API configuration
CANVAS_API_URL = 'https://canvas.uh.edu/api/v1'
ACCESS_TOKEN = '23057~o8gIcEuxleDiH3vOQCQT2AxWZlceuIdRusglN94Rf1VC7X83PD3K3ppYGIGiMlay'

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

def update_display(message, page_num, max_pages):
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
        wrapped_text = textwrap.fill(message, width=25)
        draw.text((10, 10), wrapped_text, font=font, fill=text_color)
        
        # Add arrow symbol at the bottom right corner
        arrow = [
            "     *",
            "    **",
            "   ***",
            "  ****",
            " *****",
            "******"
        ]
        arrow_height = len(arrow)
        arrow_width = len(arrow[0])
        
        for i, line in enumerate(arrow):
            draw.text((epd.width - arrow_width * 8, epd.height - arrow_height * 15 + i * 15), line, font=font, fill=text_color)
        
        # Display current page and max pages
        page_text = f"Page {page_num} of {max_pages}"
        draw.text((10, epd.height - arrow_height * 15), page_text, font=font, fill=text_color)
        
        # Display the image on the e-ink display
        epd.display(epd.getbuffer(image))

        print("Display updated successfully:", message)

    except Exception as e:
        print("Error updating display:", e)

def get_todo_items():
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
    }

    print("Fetching to-do items from Canvas API...")
    # Fetch the list of to-do items
    response = requests.get(
        f'{CANVAS_API_URL}/users/self/todo', headers=headers)

    if response.status_code == 200:
        todo_items = response.json()
        print("Fetched to-do items:", todo_items)
        return todo_items
    else: 
        print("Failed to fetch to-do items")
        return []

def create_todo_items_text(todo_items, page_num, max_items_per_page):
    start_index = (page_num - 1) * max_items_per_page
    end_index = start_index + max_items_per_page
    current_page_items = todo_items[start_index:end_index]
    
    todo_items_text = ''
    
    if current_page_items:
        todo_items_text += 'To-Do Items:\n\n'

        for item in current_page_items:
            class_name = item['assignment'].get('course', {}).get('name', 'Unknown Course')
            assignment_name = item['assignment'].get('name', 'Unknown Assignment')
            due_date_str = item['assignment'].get('due_at', '')
            due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M:%SZ') if due_date_str else None
            formatted_due_date = due_date.strftime('%m/%d/%Y') if due_date else 'Unknown Date'
            
            item_text = f"* {class_name} - {assignment_name} (Due: {formatted_due_date})\n"
            todo_items_text += item_text
    else:
        print("No to-do items available.")
        todo_items_text = "No to-do items available."
        
    print("To-do items text:", todo_items_text)
    return todo_items_text


if __name__ == "__main__":
    max_items_per_page = 2
    page_num = 1
    
    while True:
        todo_items = get_todo_items()
        
        print("To-do items:", todo_items)

        max_pages = (len(todo_items) + max_items_per_page - 1) // max_items_per_page
        
        todo_items_text = create_todo_items_text(todo_items, page_num, max_items_per_page)
        
        print("To-do items text:", todo_items_text)

        if todo_items_text:
            update_display(todo_items_text, page_num, max_pages)
        else:
            update_display("No to-do items available.", page_num, max_pages)

        # Wait for 2 minutes before checking again
        print("Waiting for 2 minutes before checking again...")
        time.sleep(300)  # Sleep for 2 minutes (300 seconds)
