from pdfminer.high_level import extract_text

pdf_path = r"c:\Users\mohib\Projects\Hackathon\Hackwithmumbai2.0 Hackathon - Segmentation Documentation.pdf"
out_path = r"c:\Users\mohib\Projects\Hackathon\Hackwithmumbai2.0 Hackathon - Segmentation Documentation.txt"

text = extract_text(pdf_path)
with open(out_path, "w", encoding="utf-8") as f:
    f.write(text)
print("EXTRACTION_DONE")
