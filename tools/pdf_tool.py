from pdf2image import convert_from_path
import pytesseract


def read_pdf(pdf_path):
    try:
        pages = convert_from_path(pdf_path)

        print(f"Pages Found: {len(pages)}")

        full_text = ""

        for i, page in enumerate(pages):
            text = pytesseract.image_to_string(page)

            print(
                f"Page {i+1} chars: {len(text)}"
            )

            full_text += text + "\n"

        return full_text

    except Exception as e:
        print("PDF ERROR:", e)
        return ""