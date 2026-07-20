from .known_en_authors import KNOWN_AUTHORS as AUTHORS
from .known_en_narrators import KNOWN_NARRATORS
from .known_translators import TRANSLATORS
from .virtual_narrators import edge_tts_narrators, google_tts_narrators

NARRATORS = KNOWN_NARRATORS | edge_tts_narrators | google_tts_narrators

__all__ = [
    "NARRATORS",
    "AUTHORS",
    "TRANSLATORS",
]
