from goodreads_normalizer.models.contributor import ContributorRole, classify_person
from goodreads_normalizer.validation.severity import Severity


class GoodreadsValidationError(ValueError):
    def __init__(self, severity: Severity, recommendation: str | None):
        self._severity = severity
        self._recommendation: str | None = recommendation

    @property
    def severity(self) -> Severity:
        return self._severity

    @property
    def recommendation(self) -> str | None:
        return self._recommendation


class NoBookTitleError(GoodreadsValidationError):
    def __init__(self):
        super().__init__(severity=Severity.ERROR, recommendation="Check Goodreads Data")

    def __str__(self):
        return "Cannot parse book title. No Title Found."


class NarratorAsAuthorError(GoodreadsValidationError):
    def __init__(self, contributor: str):
        self.contributor = contributor
        self.actual_role: ContributorRole = classify_person(contributor)

        super().__init__(severity=Severity.WARNING, recommendation=None)

    def __str__(self):
        return (
            f"{self.contributor!r} is not the primary author and is a known narrator."
        )


class NarratorAsContributorOnNonAudioEditionError(GoodreadsValidationError):
    def __init__(self, contributor: str):
        self.contributor = contributor
        self.actual_role: ContributorRole = classify_person(contributor)

        super().__init__(
            severity=Severity.WARNING,
            recommendation="Confirm your Goodreads data edition. This appears to be a non audio edition.",
        )

    def __str__(self):
        return (
            f"{self.contributor!r} is not the primary author and is a known narrator."
        )


class NoISBNWarning(GoodreadsValidationError):
    def __init__(self):
        super().__init__(severity=Severity.WARNING, recommendation=None)

    def __str__(self):
        return (
            "Book is lacking a INSB-10 or ISBN-13 identifier. This may not be required."
        )


class NoISBNError(GoodreadsValidationError):
    def __init__(self):
        super().__init__(severity=Severity.ERROR, recommendation="None")

    def __str__(self):
        return "Book is lacking a INSB-10 or ISBN-13 identifier. This is required based of binding."


class InvalidISBNError(GoodreadsValidationError):
    def __init__(self):
        super().__init__(
            severity=Severity.ERROR, recommendation="Check book data ISBN and/or ISBN13"
        )

    def __str__(self):
        return "The validation of the ISBN number found failed. This is not a correct ISBN."
