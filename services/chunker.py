import re


# ============================================================
# SECTION TITLES
# ============================================================

SECTION_TITLES = [
    "Personal Background",
    "Childhood and Early Sporting Life",
    "Domestic Cricket and Railway Career",
    "Entry into International Cricket",
    "Breakthrough: 183* Against Sri Lanka",
    "Captaincy and the 2007 T20 World Cup",
    "Test Cricket and No. 1 Ranking",
    "2011 ICC Cricket World Cup",
    "2013 ICC Champions Trophy",
    "Chennai Super Kings and IPL Legacy",
    "Test Retirement",
    "2019 World Cup",
    "International Retirement — 2020",
    "International Career Statistics",
    "Major Captaincy Achievements",
    "Wicketkeeping and Finishing",
    "Leadership Style",
    "Life After International Retirement",
    "ICC Cricket Hall of Fame",
    "Status in 2026",
    "Legacy",
    "Quick Timeline",
    "Sources",
]


# ============================================================
# PREPARE TEXT
# ============================================================

def prepare_text(text):
    """
    Ensure recognized section headings start on a new line.
    """

    for title in SECTION_TITLES:

        pattern = (
            rf"(?<!\d)"
            rf"(\d{{1,2}}\.\s*{re.escape(title)})"
        )

        text = re.sub(
            pattern,
            r"\n\1",
            text
        )

    return text


# ============================================================
# SPLIT LONG SECTION
# ============================================================

def split_long_section(section, chunk_size=700):
    """
    Split a large section without losing its heading.
    """

    section = section.strip()

    if len(section) <= chunk_size:
        return [section]

    lines = section.splitlines()

    heading = lines[0].strip()

    body = " ".join(
        line.strip()
        for line in lines[1:]
        if line.strip()
    )

    words = body.split()

    chunks = []

    current = heading

    for word in words:

        candidate = (
            current
            + " "
            + word
        )

        if len(candidate) <= chunk_size:

            current = candidate

        else:

            if current.strip():
                chunks.append(
                    current.strip()
                )

            current = (
                heading
                + " "
                + word
            )

    if current.strip():
        chunks.append(
            current.strip()
        )

    return chunks


# ============================================================
# CREATE CHUNKS
# ============================================================

def create_chunks(text, chunk_size=700):
    """
    Create meaningful chunks using recognized
    document headings.
    """

    text = prepare_text(text)

    title_pattern = "|".join(
        re.escape(title)
        for title in SECTION_TITLES
    )

    section_pattern = (
        r"(?<!\d)"
        r"(?=\d{1,2}\.\s*(?:"
        + title_pattern
        + r"))"
    )

    sections = re.split(
        section_pattern,
        text
    )

    chunks = []

    for section in sections:

        section = section.strip()

        if not section:
            continue

        section_chunks = split_long_section(
            section,
            chunk_size
        )

        chunks.extend(
            section_chunks
        )

    return chunks