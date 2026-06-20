from goodreads_normalizer.data.known_en_narrators import KNOWN_NARRATORS
from goodreads_normalizer.data.known_en_authors import KNOWN_AUTHORS
from goodreads_normalizer.data.virtual_narrators import google_tts_narrators, edge_tts_narrators


def validate_author_name(name: str) -> str:
    if (
            name in google_tts_narrators
            or name in edge_tts_narrators
            or (name in KNOWN_NARRATORS and name not in KNOWN_AUTHORS)
    ):
        raise ValueError(f"{name} is a known narrator")

    return name