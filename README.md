# RecieptAnalytics

Tidying data for future dashboard on flask website

## Instructions

1. Main Rasperry pi will run all scripts
2. Scan reciepts with hp printer
  - note: make sure to use high dpi for quality and save to google drive 'Market Receipts' folder
3. Download reciepts from gdrive and save to '/home/pi/Downloads/MarketPdf' to run: convert pdf, OCR, regex, and upload to gsheets
  - note: double check the regex results before gsheets upload
