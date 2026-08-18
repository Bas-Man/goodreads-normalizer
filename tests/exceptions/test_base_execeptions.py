from goodreads_normalizer.exceptions import base
from goodreads_normalizer.validation.severity import Severity


def test_base_exception_class() -> None:
    err = base.NarratorAsAuthorError("Travis Baldree")
    assert isinstance(err, base.NarratorAsAuthorError)
    assert err.contributor == "Travis Baldree"


def test_base_narrator_non_audio_edition() -> None:
    err = base.NarratorAsContributorOnNonAudioEditionError("Travis Baldree")
    assert isinstance(err, base.NarratorAsContributorOnNonAudioEditionError)
    assert (
        str(err)
        == "'Travis Baldree' is not the primary author and is a known narrator."
    )
    assert err.severity == Severity.WARNING
    assert (
        err.recommendation
        == "Confirm your Goodreads data edition. This appears to be a non audio edition."
    )


def test_no_title() -> None:
    err = base.NoBookTitleError()
    assert isinstance(err, base.NoBookTitleError)
    assert err.severity == Severity.ERROR
    assert err.recommendation == "Check Goodreads Data"
