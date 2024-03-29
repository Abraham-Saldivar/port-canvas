from datetime import datetime, timedelta
import requests
import textwrap
from flask import Flask, request
from flask_mail import Mail, Message
from waveshare_epd import epd2in13
from PIL import Image, ImageDraw, ImageFont
import schedule
import time
import subprocess

app = Flask(__name__)
mail = Mail(app)

# Canvas API configuration
CANVAS_API_URL = 'https://canvas.uh.edu/api/v1'
ACCESS_TOKEN = '23057~o8gIcEuxleDiH3vOQCQT2AxWZlceuIdRusglN94Rf1VC7X83PD3K3ppYGIGiMlay'
# COURSE_ID = '8637'

COURSE_IDS = ['8637', '7398', '10778', '9245']

# Function to update e-Ink display with text
def update_display(message):
    try:
        # Initialize the e-ink display
        epd = epd2in13.EPD()
        epd.init()

        # Clear the display
        epd.Clear()

        # Create a blank image with white background
        HBlackimage = Image.new('1', (epd.width, epd.height), 255)

        # Initialize drawing object
        draw = ImageDraw.Draw(HBlackimage)

        # Set font and text color
        font_size = 20
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', font_size)
        text_color = 0  # Black

        # Wrap text and draw on the image
        wrapped_text = textwrap.fill(message, width=25)
        draw.text((10, 10), wrapped_text, font=font, fill=text_color)

        # Display the image on the e-ink display
        epd.display(epd.getbuffer(HBlackimage))

    except Exception as e:
        print("Error updating display:", e)

# Function to check internet connection
def check_internet_connection():
    try:
        # Attempt to ping a reliable website (e.g., google.com)
        subprocess.run(['ping', '-c', '1', 'google.com'], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Function to get assignments from Canvas API
def get_assignments(course_id):
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
    }

    # Fetch the list of assignments for the specified course
    response = requests.get(
        f'{CANVAS_API_URL}/courses/{course_id}/assignments', headers=headers)

    if response.status_code == 200:
        assignments = response.json()
        today = datetime.now().date()

        # Filter assignments due today and for the next three days
        due_assignments = [
            assignment for assignment in assignments
            if 'due_at' in assignment and assignment['due_at'] is not None
            and today <= datetime.strptime(assignment['due_at'], '%Y-%m-%dT%H:%M:%SZ').date() <= today + timedelta(days=5)
        ]

        return due_assignments

    return []

# Function to create an image with assignments
def create_assignments_text(assignments):
    assignments_text = ''

    if assignments:
        assignments_text += 'Assignments due today and for the next 5 days:\n\n'

        for assignment in assignments:
            assignment_text = f"• {assignment['name']} \n\n"
            assignments_text += textwrap.fill(assignment_text,
                                              width=25) + '\n'
    else:
        assignments_text = 'No assignments due today and for the next 3 days.'

    return assignments_text

if __name__ == "__main__":
    while True:
        all_assignments = []

        for course_id in COURSE_IDS:
            assignments = get_assignments(course_id)
            all_assignments.extend(assignments)

        assignments_text = ''

        for assignment in all_assignments:
            assignments_text += f"{assignment['name']} \n\n"

        # Check internet connection
        if check_internet_connection():
            if assignments_text:
                update_display(assignments_text)
            else:
                update_display("No assignments available.")
        else:
            update_display("No internet connection.")

        # Wait for 2 minutes before checking again
        time.sleep(120)  # Sleep for 2 minutes (120 seconds)
