# Shopify Sync

A Python script for syncing product data from Google Sheets to Shopify. Product photos can be loaded either from Google Drive or from the local `local_photo` folder.

## What this project does

- reads product data from Google Sheets;
- loads product photos from Google Drive or from a local folder;
- creates products in Shopify;
- adds product images, tags, variants, and metafields;
- stores temporary sync data in a local SQLite database: `data.db`.

## Project structure

```text
.
├── core/                 # Google Drive, Google Sheets, and helper functions
├── db/                   # Peewee/SQLite database models
├── module/               # Additional Shopify modules, such as metafields
├── drive_photo/          # Photos downloaded from Google Drive
├── local_photo/          # Local product photos for Shopify upload
├── main.py               # Main script entry point
├── settings.example.py   # Example configuration file
├── requirements.txt      # Python dependencies
└── README.md
```

## Setup

### 1. Install Python

Use Python 3.9 or newer.

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

macOS/Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the settings file

Copy the example settings file:

```bash
cp settings.example.py settings.py
```

On Windows, you can also copy `settings.example.py` manually and rename the copy to `settings.py`.

Then fill in your own Google API and Shopify API values inside `settings.py`.

### 5. Add Google API credential files

Place your private Google credential files in the project root:

```text
gsh_acc.json
gdv_acc.json
client_secrets.json
```

These files contain private keys and tokens. Do not commit them to GitHub.

## Local photo structure

If you choose to upload photos from the local folder, the `local_photo` directory should be organized like this:

```text
local_photo/
├── 1001/
│   ├── 1.jpg
│   ├── 2.jpg
│   └── 3.jpg
├── 1002/
│   ├── 1.jpg
│   └── 2.jpg
```

Each folder name should match the product lot number from Google Sheets.

## Important: updating photos in `local_photo`

Before every new photo update in the `local_photo` folder, delete the `data.db` file from the project root.

This is required because the script saves information about already found and processed photos in the local SQLite database. If you replace or update photos but keep the old `data.db`, the script may think that the photos were already processed and may not detect the new files correctly.

Recommended workflow for updating local photos:

1. Stop the script if it is running.
2. Update or replace photos inside `local_photo`.
3. Delete `data.db` from the project root.
4. Run `main.py` again.

The database will be created again automatically when the script starts, using the models from `db/models.py`.

## Running the project

```bash
python main.py
```

After launch, the script asks where to load photos from:

```text
From Google Drive - 1 | Locally - 2
```

Then it asks you to choose the Google Sheets worksheet and starts the sync process.

## Security note

Never publish real API keys, Shopify tokens, Google service account files, or OAuth secrets in a public repository.

If these credentials were ever uploaded to GitHub or shared publicly, revoke them and generate new ones.
