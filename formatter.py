import textwrap

MAX_CHARS_PER_LINE =    47
MAX_LINES_PER_PAGE =    10
CHAR_WIDTH =            6           # 5 + 1 for spacing
CHAR_HEIGHT =           8           # 7 + 1 for spacing
PAGE_WIDTH =            296         
PAGE_HEIGHT =           128         

def is_chapter_header(line: str) -> bool:
    line = line.strip()
    return (
        line.lower().startswith("chapter")
    )

# returns a list of lines, each ended with newline char
def wrap_paragraph(paragraph: str) -> list[str]:
    wrapped = textwrap.fill(
        paragraph,
        width=MAX_CHARS_PER_LINE,
        replace_whitespace=True,
        drop_whitespace=True,
    )
    return wrapped.split("\n")

# splits lines into list of pages
# NOTE: respects paragraph breaks in the original file
def paginate_lines(lines: list[str]) -> list[list[str]]:
    pages = []
    current_page = []

    for line in lines:
        current_page.append(line)
        if len(current_page) >= MAX_LINES_PER_PAGE:
            pages.append(current_page)
            current_page = []

    if current_page:
        pages.append(current_page)

    return pages

def process_text(lines: list[str]) -> list[list[str]]:
    pages = []
    current_lines = []
    paragraph_buffer = []

    def flush_paragraph():
        nonlocal current_lines, paragraph_buffer
        if paragraph_buffer:
            wrapped = wrap_paragraph(" ".join(paragraph_buffer))
            current_lines.extend(wrapped)
            current_lines.append("")  # blank line after paragraph
            paragraph_buffer.clear()

    def flush_page():
        nonlocal current_lines
        if current_lines:
            pages.extend(paginate_lines(current_lines))
            current_lines = []

    i = 0
    while i < len(lines):
        raw_line = lines[i]
        line = raw_line.rstrip("\n")

        if is_chapter_header(line.strip()):
            flush_paragraph()
            flush_page()

            chapter_page = [""] * MAX_LINES_PER_PAGE
            mid = MAX_LINES_PER_PAGE // 2

            chapter_page[mid - 1] = line.strip().center(MAX_CHARS_PER_LINE)

            # Check if next line exists and is not blank
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line != "":
                    chapter_page[mid] = next_line.center(MAX_CHARS_PER_LINE)
                    i += 1  # consume the subtitle line

            pages.append(chapter_page)
            i += 1
            continue


        # Paragraph break
        if line.strip() == "":
            flush_paragraph()
            i += 1
            continue

        paragraph_buffer.append(line.lstrip())

        i += 1

    # Flush remaining content
    flush_paragraph()
    flush_page()

    return pages



from pathlib import Path

# ---- configuration ----
INPUT_FILE = "fellowship.txt"
OUTPUT_FILE = "fellowship_paged.txt"

def main():
    input_path = Path(INPUT_FILE)
    output_path = input_path.with_name(OUTPUT_FILE)

    # Read input
    with input_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    # Process text into pages
    pages = process_text(lines)

    # Write output
    with output_path.open("w", encoding="utf-8") as f:
        for i, page in enumerate(pages):
            for line in page:
                f.write(line + "\n")
            f.write("<<PAGE BREAK>>\n")

    print(f"Wrote {len(pages)} pages to {output_path}")

if __name__ == "__main__":
    main()

