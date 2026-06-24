# 🎓 Automated Certificate Generator \& Email Sender

Generate personalized certificates from a CSV file and automatically email them to participants.

## Features

* Dynamic certificate generation
* Automatic name centering
* Automatic font resizing
* Bulk email delivery
* Duplicate email protection
* HTML formatted emails
* Progress tracking with tqdm

\---

## Installation

```bash
git clone https://github.com/yourusername/certificate-generator.git
cd certificate-generator

pip install -r requirements.txt
```

\---

## Configuration

Create a `.env` file from `.env.example`

```env
SENDER\_EMAIL=your\_email@gmail.com
APP\_PASSWORD=your\_app\_password

CSV\_FILE=data/participants.csv
TEMPLATE\_FILE=assets/certificate\_template.png
FONT\_FILE=assets/arialbd.ttf
```

\---

## Gmail App Password Setup

Google no longer allows using your normal account password for SMTP.

### Step 1: Enable 2-Factor Authentication

1. Go to your Google Account
2. Select Security
3. Enable 2-Step Verification

### Step 2: Generate an App Password

1. Go to:
https://myaccount.google.com/apppasswords
2. Sign in if prompted
3. Under:

   * Select App → Mail
   * Select Device → Other
4. Enter:

```
   Certificate Generator
   ```

5. Click Generate

Google will provide a 16-character password:

```
abcd efgh ijkl mnop
```

Use this value as:

```env
APP\_PASSWORD=abcd efgh ijkl mnop
```

⚠️ Never commit your real App Password to GitHub.

\---

## CSV Format

```csv
first\_name,last\_name,email
John,Doe,john@example.com
Jane,Smith,jane@example.com
```

\---

## Run

```bash
python certi\_gen.py
```

\---

## Output

Generated certificates are saved inside:

```text
certificates/
```

\---

## Drawbacks

* Gmail can send upto 500 emails per day only so if more than 500 then you will have to use another account or wait for 24 hrs for the limit to reset

## Security Notes

* Never commit `.env`
* Never commit App Passwords
* Rotate credentials regularly
* Use GitHub Secrets for CI/CD

\---

## Author

Aditya D
Founder - OS.dev

