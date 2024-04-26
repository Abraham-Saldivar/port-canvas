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
import random
from TP_lib import gt1151
from TP_lib import epd2in13_V4 as epd2in13
from PIL import Image, ImageDraw, ImageFont
import textwrap
import time
import threading


# Constants
LOCAL_WORDS = [
    {'word': 'aberration', 'definition': 'a departure from what is normal, usual, or expected, typically one that is unwelcome'},
    {'word': 'alacrity', 'definition': 'brisk and cheerful readiness'},
    {'word': 'anachronistic', 'definition': 'belonging to a period other than that being portrayed'},
    {'word': 'anomaly', 'definition': 'something that deviates from what is standard, normal, or expected'},
    {'word': 'antebellum', 'definition': 'occurring or existing before a particular war, especially the American Civil War'},
    {'word': 'antediluvian', 'definition': 'of or belonging to the time before the biblical Flood'},
    {'word': 'apocryphal', 'definition': 'of doubtful authenticity, although widely circulated as being true'},
    {'word': 'arcane', 'definition': 'understood by few; mysterious or secret'},
    {'word': 'assiduous', 'definition': 'showing great care and perseverance'},
    {'word': 'astute', 'definition': 'having or showing an ability to accurately assess situations or people and turn this to one\'s advantage'},
    {'word': 'benevolent', 'definition': 'well-meaning and kindly'},
    {'word': 'bucolic', 'definition': 'relating to the pleasant aspects of the countryside and country life'},
    {'word': 'capitulate', 'definition': 'cease to resist an opponent or an unwelcome demand; surrender'},
    {'word': 'circumlocution', 'definition': 'the use of many words where fewer would do, especially in a deliberate attempt to be vague or evasive'},
    {'word': 'cogent', 'definition': 'clear, logical, and convincing'},
    {'word': 'commensurate', 'definition': 'corresponding in size or degree; in proportion'},
    {'word': 'conflagration', 'definition': 'an extensive fire that destroys a great deal of land or property'},
    {'word': 'conundrum', 'definition': 'a confusing and difficult problem or question'},
    {'word': 'copious', 'definition': 'abundant in supply or quantity'},
    {'word': 'deleterious', 'definition': 'causing harm or damage'},
    {'word': 'diatribe', 'definition': 'a forceful and bitter verbal attack against someone or something'},
    {'word': 'disparate', 'definition': 'essentially different in kind; not allowing comparison'},
    {'word': 'eclectic', 'definition': 'deriving ideas, style, or taste from a broad and diverse range of sources'},
    {'word': 'ebullient', 'definition': 'cheerful and full of energy'},
    {'word': 'egalitarian', 'definition': 'believing in or based on the principle that all people are equal and deserve equal rights and opportunities'},
    {'word': 'empathy', 'definition': 'the ability to understand and share the feelings of another'},
    {'word': 'enervate', 'definition': 'cause (someone) to feel drained of energy or vitality; weaken'},
    {'word': 'enfranchise', 'definition': 'give the right to vote to'},
    {'word': 'ephemeral', 'definition': 'lasting for a very short time'},
    {'word': 'equanimity', 'definition': 'mental calmness, composure, and evenness of temper, especially in a difficult situation'},
    {'word': 'esoteric', 'definition': 'intended for or likely to be understood by only a small number of people with a specialized knowledge or interest'},
    {'word': 'euphemism', 'definition': 'a mild or indirect word or expression substituted for one considered to be too harsh or blunt when referring to something unpleasant or embarrassing'},
    {'word': 'evanescent', 'definition': 'soon passing out of sight, memory, or existence; quickly fading or disappearing'},
    {'word': 'exacerbate', 'definition': 'make (a problem, bad situation, or negative feeling) worse'},
    {'word': 'exculpate', 'definition': 'show or declare that (someone) is not guilty of wrongdoing'},
    {'word': 'exonerate', 'definition': 'absolve (someone) from blame for a fault or wrongdoing'},
    {'word': 'fervent', 'definition': 'having or displaying a passionate intensity'},
    {'word': 'garrulous', 'definition': 'excessively talkative, especially on trivial matters'},
    {'word': 'gregarious', 'definition': 'fond of company; sociable'},
    {'word': 'hackneyed', 'definition': '(of a phrase or idea) lacking significance through having been overused; unoriginal and trite'},
    {'word': 'harangue', 'definition': 'a lengthy and aggressive speech'},
    {'word': 'impecunious', 'definition': 'having little or no money'},
    {'word': 'incendiary', 'definition': 'tending to stir up conflict'},
    {'word': 'incorrigible', 'definition': '(of a person or their tendencies) not able to be corrected, improved, or reformed'},
    {'word': 'indolent', 'definition': 'wanting to avoid activity or exertion; lazy'},
    {'word': 'ineffable', 'definition': 'too great or extreme to be expressed or described in words'},
    {'word': 'insidious', 'definition': 'proceeding in a gradual, subtle way, but with harmful effects'},
    {'word': 'inure', 'definition': 'accustom (someone) to something, especially something unpleasant'},
    {'word': 'inveterate', 'definition': 'having a particular habit, activity, or interest that is long-established and unlikely to change'},
    {'word': 'juxtapose', 'definition': 'place or deal with close together for contrasting effect'},
    {'word': 'lucid', 'definition': 'expressed clearly; easy to understand'},
    {'word': 'maudlin', 'definition': 'self-pityingly or tearfully sentimental, often through drunkenness'},
    {'word': 'mawkish', 'definition': 'sentimental in a feeble or sickly way'},
    {'word': 'modicum', 'definition': 'a small quantity of a particular thing, especially something considered desirable or valuable'},
    {'word': 'munificent', 'definition': 'larger or more generous than is usual or necessary'},
    {'word': 'nefarious', 'definition': '(typically of an action or activity) wicked or criminal'},
    {'word': 'obtuse', 'definition': 'annoyingly insensitive or slow to understand'},
    {'word': 'onerous', 'definition': '(of a task or responsibility) involving a great deal of effort, trouble, or difficulty'},
    {'word': 'pariah', 'definition': 'an outcast'},
    {'word': 'pedantic', 'definition': 'excessively concerned with minor details or rules; overscrupulous'},
    {'word': 'penchant', 'definition': 'a strong or habitual liking for something or tendency to do something'},
    {'word': 'perfidious', 'definition': 'deceitful and untrustworthy'},
    {'word': 'perfunctory', 'definition': '(of an action or gesture) carried out with a minimum of effort or reflection'},
    {'word': 'perspicacious', 'definition': 'having a ready insight into and understanding of things'},
    {'word': 'plethora', 'definition': 'a large or excessive amount of something'},
    {'word': 'precocious', 'definition': '(of a child) having developed certain abilities or proclivities at an earlier age than usual'},
    {'word': 'prescient', 'definition': 'having or showing knowledge of events before they take place'},
    {'word': 'proclivity', 'definition': 'a tendency to choose or do something regularly; an inclination or predisposition toward a particular thing'},
    {'word': 'prodigious', 'definition': 'remarkably or impressively great in extent, size, or degree'},
    {'word': 'profligate', 'definition': 'recklessly extravagant or wasteful in the use of resources'},
    {'word': 'propensity', 'definition': 'an inclination or natural tendency to behave in a particular way'},
    {'word': 'prudent', 'definition': 'acting with or showing care and thought for the future'},
    {'word': 'quixotic', 'definition': 'exceedingly idealistic; unrealistic and impractical'},
    {'word': 'recalcitrant', 'definition': 'having an obstinately uncooperative attitude towards authority or discipline'},
    {'word': 'redolent', 'definition': 'strongly reminiscent or suggestive of (something)'},
    {'word': 'replete', 'definition': 'filled or well-supplied with something'},
    {'word': 'resilient', 'definition': 'able to recoil or spring back into shape after bending, stretching, or being compressed'},
    {'word': 'sagacious', 'definition': 'having or showing keen mental discernment and good judgment; wise or shrewd'},
    {'word': 'salient', 'definition': 'most noticeable or important'},
    {'word': 'sanguine', 'definition': 'optimistic or positive, especially in an apparently bad or difficult situation'},
    {'word': 'sardonic', 'definition': 'grimly mocking or cynical'},
    {'word': 'soporific', 'definition': 'tending to induce drowsiness or sleep'},
    {'word': 'spurious', 'definition': 'not being what it purports to be; false or fake'},
    {'word': 'strident', 'definition': 'loud and harsh; grating'},
    {'word': 'superfluous', 'definition': 'unnecessary, especially through being more than enough'},
    {'word': 'taciturn', 'definition': '(of a person) reserved or uncommunicative in speech; saying little'},
    {'word': 'tenuous', 'definition': 'very weak or slight'},
    {'word': 'timorous', 'definition': 'showing or suffering from nervousness, fear, or a lack of confidence'},
    {'word': 'ubiquitous', 'definition': 'present, appearing, or found everywhere'},
    {'word': 'umbrage', 'definition': 'offense or annoyance'},
    {'word': 'unctuous', 'definition': '(of a person) excessively or ingratiatingly flattering; oily'},
    {'word': 'untoward', 'definition': 'unexpected and inappropriate or inconvenient'},
    {'word': 'vacuous', 'definition': 'having or showing a lack of thought or intelligence; mindless'},
    {'word': 'venerable', 'definition': 'accorded a great deal of respect, especially because of age, wisdom, or character'},
    {'word': 'vex', 'definition': 'make (someone) feel annoyed, frustrated, or worried, especially with trivial matters'},
    {'word': 'vicarious', 'definition': 'experienced in the imagination through the feelings or actions of another person'},
    {'word': 'vilify', 'definition': 'speak or write about in an abusively disparaging manner'},
    {'word': 'visceral', 'definition': 'relating to deep inward feelings rather than to the intellect'},
    {'word': 'vitriolic', 'definition': 'filled with bitter criticism or malice'},
    {'word': 'winsome', 'definition': 'attractive or appealing in appearance or character'},
    {'word': 'zealot', 'definition': 'a person who is fanatical and uncompromising in pursuit of their religious, political, or other ideals'},
]



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
    "And the LORD God commanded the man, saying, 'You may surely eat of every tree of the garden, - Genesis 2:16",
    "But of the tree of the knowledge of good and evil you shall not eat, for in the day that you eat of it you shall surely die.' - Genesis 2:17",
    "Then the LORD God said, 'It is not good that the man should be alone; I will make him a helper fit for him.' - Genesis 2:18",
    "So out of the ground the LORD God formed every beast of the field and every bird of the heavens and brought them to the man to see what he would call them. And whatever the man called every living creature, that was its name. - Genesis 2:19",
    "The man gave names to all livestock and to the birds of the heavens and to every beast of the field. But for Adam there was not found a helper fit for him. - Genesis 2:20",
    "So the LORD God caused a deep sleep to fall upon the man, and while he slept took one of his ribs and closed up its place with flesh. - Genesis 2:21",
    "And the rib that the LORD God had taken from the man he made into a woman and brought her to the man. - Genesis 2:22",
    "Then the man said, 'This at last is bone of my bones and flesh of my flesh; she shall be called Woman, because she was taken out of Man.' - Genesis 2:23",
    "Therefore a man shall leave his father and his mother and hold fast to his wife, and they shall become one flesh. - Genesis 2:24",
    "And the man and his wife were both naked and were not ashamed. - Genesis 2:25",
    "Now the serpent was more crafty than any other beast of the field that the LORD God had made. He said to the woman, 'Did God actually say, ‘You shall not eat of any tree in the garden’?' - Genesis 3:1",
    "And the woman said to the serpent, 'We may eat of the fruit of the trees in the garden, - Genesis 3:2",
    "but God said, ‘You shall not eat of the fruit of the tree that is in the midst of the garden, neither shall you touch it, lest you die.’ - Genesis 3:3",
    "But the serpent said to the woman, 'You will not surely die. - Genesis 3:4",
    "For God knows that when you eat of it your eyes will be opened, and you will be like God, knowing good and evil.' - Genesis 3:5",
    "So when the woman saw that the tree was good for food, and that it was a delight to the eyes, and that the tree was to be desired to make one wise, she took of its fruit and ate, and she also gave some to her husband who was with her, and he ate. - Genesis 3:6",
    "Then the eyes of both were opened, and they knew that they were naked. And they sewed fig leaves together and made themselves loincloths. - Genesis 3:7",
    "And they heard the sound of the LORD God walking in the garden in the cool of the day, and the man and his wife hid themselves from the presence of the LORD God among the trees of the garden. - Genesis 3:8",
    "But the LORD God called to the man and said to him, 'Where are you?' - Genesis 3:9",
    "And he said, 'I heard the sound of you in the garden, and I was afraid, because I was naked, and I hid myself.' - Genesis 3:10",
    "He said, 'Who told you that you were naked? Have you eaten of the tree of which I commanded you not to eat?' - Genesis 3:11",
    "The man said, 'The woman whom you gave to be with me, she gave me fruit of the tree, and I ate.' - Genesis 3:12",
    "Then the LORD God said to the woman, 'What is this that you have done?' The woman said, 'The serpent deceived me, and I ate.' - Genesis 3:13",
    "The LORD God said to the serpent, 'Because you have done this, cursed are you above all livestock and above all beasts of the field; on your belly you shall go, and dust you shall eat all the days of your life. - Genesis 3:14",
    "I will put enmity between you and the woman, and between your offspring and her offspring; he shall bruise your head, and you shall bruise his heel.' - Genesis 3:15",
    "To the woman he said, 'I will surely multiply your pain in childbearing; in pain you shall bring forth children. Your desire shall be contrary to your husband, but he shall rule over you.' - Genesis 3:16",
    "And to Adam he said, 'Because you have listened to the voice of your wife and have eaten of the tree of which I commanded you, ‘You shall not eat of it,’ cursed is the ground because of you; in pain you shall eat of it all the days of your life; - Genesis 3:17",
    "thorns and thistles it shall bring forth for you; and you shall eat the plants of the field. - Genesis 3:18",
    "By the sweat of your face you shall eat bread, till you return to the ground, for out of it you were taken; for you are dust, and to dust you shall return.' - Genesis 3:19",
    "The man called his wife's name Eve, because she was the mother of all living. - Genesis 3:20",
    "And the LORD God made for Adam and for his wife garments of skins and clothed them. - Genesis 3:21",
    "Then the LORD God said, 'Behold, the man has become like one of us in knowing good and evil. Now, lest he reach out his hand and take also of the tree of life and eat, and live forever—' - Genesis 3:22",
    "therefore the LORD God sent him out from the garden of Eden to work the ground from which he was taken. - Genesis 3:23",
    "He drove out the man, and at the east of the garden of Eden he placed the cherubim and a flaming sword that turned every way to guard the way to the tree of life. - Genesis 3:24",
    "Now Adam knew Eve his wife, and she conceived and bore Cain, saying, 'I have gotten a man with the help of the LORD.' - Genesis 4:1",
    "And again, she bore his brother Abel. Now Abel was a keeper of sheep, and Cain a worker of the ground. - Genesis 4:2",
    "In the course of time Cain brought to the LORD an offering of the fruit of the ground, - Genesis 4:3",
    "and Abel also brought of the firstborn of his flock and of their fat portions. And the LORD had regard for Abel and his offering, - Genesis 4:4",
    "but for Cain and his offering he had no regard. So Cain was very angry, and his face fell. - Genesis 4:5",
    "The LORD said to Cain, 'Why are you angry, and why has your face fallen? - Genesis 4:6",
    "If you do well, will you not be accepted? And if you do not do well, sin is crouching at the door. Its desire is contrary to you, but you must rule over it.' - Genesis 4:7",
    "Cain spoke to Abel his brother. And when they were in the field, Cain rose up against his brother Abel and killed him. - Genesis 4:8",
    "Then the LORD said to Cain, 'Where is Abel your brother?' He said, 'I do not know; am I my brother's keeper?' - Genesis 4:9",
    "And the LORD said, 'What have you done? The voice of your brother's blood is crying to me from the ground. - Genesis 4:10",
    "And now you are cursed from the ground, which has opened its mouth to receive your brother's blood from your hand. - Genesis 4:11"
]
def get_random_word():
    word_data = random.choice(LOCAL_WORDS)
    return word_data['word'], word_data['definition']


# Initialize e-ink display
epd = epd2in13.EPD()
gt = gt1151.GT1151()
GT_Dev = gt1151.GT_Development()
GT_Old = gt1151.GT_Development()
# Function to update display with the next verse or word
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
        
        global current_verse_index
        current_verse_index = (current_verse_index + 1) % len(verses)
        current_item = verses[current_verse_index]
        
        if current_verse_index % 2 == 0:
            # Display verse
            wrapped_text = textwrap.fill(current_item, width=25)
            draw.text((10, 10), wrapped_text, font=font, fill=text_color)
        else:
            # Display random word
            word, definition = get_random_word()
            wrapped_definition = textwrap.fill(definition, width=25)
            draw.text((10, 10), f"Word of the Day:", font=font, fill=text_color)
            draw.text((10, 40), f"{word}:", font=font, fill=text_color)
            draw.text((10, 70), f"{wrapped_definition}", font=font, fill=text_color)
        
        # Display the image on the e-ink display
        epd.display(epd.getbuffer(image))

        print("Display updated successfully")

    except Exception as e:
        print("Error updating display:", e)
# Function to update display with the next verse
# def update_display():
#     try:
#         print("Updating display...")
#         epd.init(epd.FULL_UPDATE)
#         epd.Clear(0xFF)
        
#         # Initialize image
#         image = Image.new('1', (epd.height, epd.width), 255)
#         draw = ImageDraw.Draw(image)
        
#         # Set font and text color
#         font_size = 12
#         text_color = 0  # Black
#         font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', font_size)
        
#         # Get the next verse
#         global current_verse_index
#         current_verse_index = (current_verse_index + 1) % len(verses)
#         current_verse = verses[current_verse_index]
        
#         # Wrap text and draw on the image
#         wrapped_text = textwrap.fill(current_verse, width=25)
#         draw.text((10, 10), wrapped_text, font=font, fill=text_color)
        
#         # Display the image on the e-ink display
#         epd.display(epd.getbuffer(image))

#         print("Display updated successfully with verse:", current_verse)

#     except Exception as e:
#         print("Error updating display:", e)

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


