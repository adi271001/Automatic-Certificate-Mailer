import os
import time
import smtplib
import pandas as pd

from tqdm import tqdm
from PIL import Image, ImageDraw, ImageFont
from email.message import EmailMessage

SENDER_EMAIL = "<sender email>"
APP_PASSWORD = "<app password>"

CSV_FILE = "<path to csv file>"
TEMPLATE_FILE = "<path to certificate template file>"
FONT_FILE = "arialbd.ttf"

OUTPUT_FOLDER = "certificates"
SENT_LOG_FILE = "sent_log.txt"

EMAIL_SUBJECT = "<Subject of Email"
CENTER_X = 635
NAME_Y = 455
MAX_FONT_SIZE = 72
MIN_FONT_SIZE = 40
ERASE_BOX = [(330, 410), (930, 570)]
EMAIL_DELAY = 5

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
sent_emails = set()

if os.path.exists(SENT_LOG_FILE):
    with open(SENT_LOG_FILE, "r", encoding="utf-8") as f:
        sent_emails = set(line.strip() for line in f)

df = pd.read_csv(CSV_FILE)
#my sheet had names in the form of two columns first and last name change as per your sheet
FIRST_NAME_COLUMN = "first_name"
LAST_NAME_COLUMN = "last_name"
EMAIL_COLUMN = "email"

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

    smtp.login(SENDER_EMAIL, APP_PASSWORD)

    for _, row in tqdm(df.iterrows(), total=len(df)):

        first_name = str(row[FIRST_NAME_COLUMN]).strip()
        last_name = str(row[LAST_NAME_COLUMN]).strip()

        if first_name.lower() == "nan":
            first_name = ""

        if last_name.lower() == "nan":
            last_name = ""

        name = " ".join(
            part for part in [first_name, last_name]
            if part
        )

        email = str(row[EMAIL_COLUMN]).strip()

        if email in sent_emails:
            print(f"Skipping {email} (already sent)")
            continue

        image = Image.open(TEMPLATE_FILE)

        draw = ImageDraw.Draw(image)

        draw.rectangle(
            ERASE_BOX,
            fill="white"
        )

        font_size = MAX_FONT_SIZE

        while font_size >= MIN_FONT_SIZE:

            font = ImageFont.truetype(
                FONT_FILE,
                font_size
            )

            bbox = draw.textbbox(
                (0, 0),
                name,
                font=font
            )

            width = bbox[2] - bbox[0]

            if width < 520:
                break

            font_size -= 2

        x = CENTER_X - width / 2
        draw.text(
            (x, NAME_Y),
            name,
            fill="black",
            font=font
        )

        safe_name = (
            name.replace("/", "-")
                .replace("\\", "-")
                .replace(":", "")
                .replace("*", "")
                .replace("?", "")
        )

        filename = f"{safe_name}.png"

        filepath = os.path.join(
            OUTPUT_FOLDER,
            filename
        )

        image.save(filepath)
        msg = EmailMessage()

        msg["Subject"] = EMAIL_SUBJECT
        msg["From"] = SENDER_EMAIL
        msg["To"] = email

        msg.set_content(
            f"Dear {name}, please view this email in HTML format."
        )

        html_body = f"""<html code which acts as body of the email for example thanking participants for joining events"""

        msg.add_alternative(
            html_body,
            subtype="html"
        )

        with open(filepath, "rb") as f:

            msg.add_attachment(
                f.read(),
                maintype="image",
                subtype="png",
                filename=filename
            )

        try:

            smtp.send_message(msg)

            print(f"✓ Sent to {email}")

            with open(
                SENT_LOG_FILE,
                "a",
                encoding="utf-8"
            ) as log:

                log.write(email + "\n")

            sent_emails.add(email)

            time.sleep(EMAIL_DELAY)

        except Exception as e:

            print(f"❌ Failed for {email}")
            print(e)

print("\n✅ All certificates processed successfully.")
