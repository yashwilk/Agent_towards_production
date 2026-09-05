"""Configuration for the hushvert file-conversion client."""

import os

from dotenv import load_dotenv

load_dotenv()

HUSHVERT_API = "https://hushvert.com/api"
HUSHVERT_API_KEY = os.environ.get("HUSHVERT_API_KEY")

SAMPLE_DOCX_PATH = "vendor_review.docx"
