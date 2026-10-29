from pdf2image import convert_from_path
import fitz
import pytesseract


def read_pdf(pdf_path):
    full_text = ""

    try:
        with fitz.open(pdf_path) as doc:
            total_pages = len(doc)

        print(f"Pages Found: {total_pages}")

        for page_num in range(1, total_pages + 1):
            images = convert_from_path(
                pdf_path,
                first_page=page_num,
                last_page=page_num,
                dpi=150,
            )

            if not images:
                raise RuntimeError(
                    f"Failed to render PDF page {page_num}"
                )

            try:
                text = pytesseract.image_to_string(images[0])
            finally:
                for image in images:
                    image.close()

            print(f"Page {page_num}/{total_pages}: {len(text)} chars")
            full_text += text + "\n"

        return full_text

    except Exception as e:
        print(f"PDF ERROR: {e}")
        raise
