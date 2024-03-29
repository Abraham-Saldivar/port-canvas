from datetime import datetime, timedelta
import requests
import textwrap
from TP_lib import gt1151
from TP_lib import epd2in13_V4 as epd2in13
import time
import logging
from PIL import Image, ImageDraw, ImageFont

# Canvas API configuration
CANVAS_API_URL = 'https://canvas.uh.edu/api/v1'
ACCESS_TOKEN = '23057~o8gIcEuxleDiH3vOQCQT2AxWZlceuIdRusglN94Rf1VC7X83PD3K3ppYGIGiMlay'
COURSE_IDS = ['8637', '7398', '10778', '9245']

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

def update_display(message):
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

        # Wrap text and draw on the image
        wrapped_text = textwrap.fill(message, width=25)
        draw.text((10, 10), wrapped_text, fill=text_color)
        
        # Display the image on the e-ink display
        epd.display(epd.getbuffer(image))

        print("Display updated successfully:", message)

    except Exception as e:
        print("Error updating display:", e)

def get_assignments(course_id):
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
    }

    print("Fetching assignments from Canvas API...")
    # Fetch the list of assignments for the specified course
    response = requests.get(
        f'{CANVAS_API_URL}/courses/{course_id}/assignments', headers=headers)

    if response.status_code == 200:
        assignments = response.json()
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        day_after_tomorrow = today + timedelta(days=2)
        
        print("Today:", today)
        print("Tomorrow:", tomorrow)
        print("Day after tomorrow:" ,day_after_tomorrow)
        
        # Filter assignments due today and for the next three days
        due_assignments = [
            assignment for assignment in assignments
            if 'due_at' in assignment and assignment['due_at'] is not None
            and (datetime.strptime(assignment['due_at'], '%Y-%m-%dT%H:%M:%SZ').date() in [today, tomorrow, day_after_tomorrow])
        ]
        
        print("Due Assigments:")
        for assign in assignments:
            print(f" - {assign['name']}: {assign['due_at']}")
        
        return due_assignments
    else: 
        print("Failed to fetch assigments")
        return []

def create_assignments_text(assignments):
    assignments_text = ''
    
    if assignments:
        assignments_text += 'Assignments due today and for the next 3 days:\n\n'

        for assign in assignments:
            due_date = datetime.strptime(assign['due_at'],'%Y-%m-%dT%H:%M:%SZ').date()
            
            # Format the date 
            
            if due_date == datetime.now().date():
                due_date_text = datetime.strptime(assign['due_at'],'%Y-%m-%dT%H:%M:%SZ').strftime('%H:%M') + " today"
            
            else: 
                due_date_text = due_date.strftime('%m/%d/%Y')
                
            assignment_text = f"* {assign['name']} (Due: {due_date_text})\n"
            assignments_text += assignment_text
    else:
        assignments_text = "No assignments available for today and for the next 3 days."

    return assignments_text

if __name__ == "__main__":
    epd = epd2in13.EPD()
    gt = gt1151.GT1151()
    GT_Dev = gt1151.GT_Development()
    GT_Old = gt1151.GT_Development()
    
    t = threading.Thread(target = pthread_irq)
    t.setDaemon(True)
    t.start()

    while True:
        all_assignments = []

        for course_id in COURSE_IDS:
            assignments = get_assignments(course_id)
            all_assignments.extend(assignments)

        assignments_text = create_assignments_text(all_assignments)

        if assignments_text:
            update_display(assignments_text)
        else:
            update_display("No assignments available for today and for the next 3 days.")

        # Wait for 2 minutes before checking again
        print("Waiting for 2 minutes before checking again...")
        time.sleep(120)  # Sleep for 2 minutes (120 seconds)
