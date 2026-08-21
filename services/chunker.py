import re


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


def prepare_text(text):
    """
    Put each known section heading on a new line.
    """

    for index, title in enumerate(SECTION_TITLES, start=1):

        pattern = rf"(?<!\d){index}\.\s*{re.escape(title)}"

        replacement = f"\n{index}. {title}"

        text = re.sub(
            pattern,
            replacement,
            text
        )

    return text


def split_long_text(text, chunk_size):
    """
    Split large sections without cutting words.
    """

    words = text.split()

    chunks = []
    current_chunk = ""

    for word in words:

        if not current_chunk:

            current_chunk = word

            continue

        candidate = (
            current_chunk
            + " "
            + word
        )

        if len(candidate) <= chunk_size:

            current_chunk = candidate

        else:

            chunks.append(
                current_chunk.strip()
            )

            current_chunk = word

    if current_chunk:

        chunks.append(
            current_chunk.strip()
        )

    return chunks


def create_chunks(text, chunk_size=700):
    """
    Create chunks using the document's known
    section structure.
    """

    text = prepare_text(text)

    heading_pattern = (
        r"(?m)(?=^\d{1,2}\.\s+)"
    )

    sections = re.split(
        heading_pattern,
        text
    )

    chunks = []

    for section in sections:

        section = section.strip()

        if not section:
            continue

        if len(section) <= chunk_size:

            chunks.append(section)

        else:

            chunks.extend(
                split_long_text(
                    section,
                    chunk_size
                )
            )

    return chunks