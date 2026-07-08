import os
from pathlib import Path
from datetime import datetime

async def get_date():
    return datetime.now().strftime("%H:%M:%S")