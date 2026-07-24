from enum import Enum

_AUDIOBOOK_KEYWORDS = ("audio", "mp3 cd")
_PRINT_MEDIA_KEYWORDS_HARDCOVER = ("hardcover", "hardback")
_PRINT_MEDIA_KEYWORDS_PAPERBACK = ("paperback", "trade paper")


class BindingFormat(Enum):
    """Normalized binding/format classification for a Goodreads book entry."""

    HARDCOVER = "hardcover"
    PAPERBACK = "paperback"
    KINDLE = "kindle"
    EBOOK = "ebook"
    AUDIOBOOK = "audiobook"
    UNKNOWN = "unknown"

    @classmethod
    def from_str(cls, binding: str | None) -> "BindingFormat":
        """Classify a raw Goodreads binding string into a BindingFormat.

        Args:
            binding: Raw binding string from the Goodreads CSV
                (e.g. "Audible Audio", "MP3 CD", "Kindle Edition").

        Returns:
            The matching BindingFormat, or UNKNOWN if unrecognized.
        """
        if binding is None:
            return cls.UNKNOWN

        binding_lower = binding.lower()

        if any(k in binding_lower for k in _AUDIOBOOK_KEYWORDS):
            return cls.AUDIOBOOK
        if "kindle" in binding_lower:
            return cls.KINDLE
        if any(k in binding_lower for k in _PRINT_MEDIA_KEYWORDS_HARDCOVER):
            return cls.HARDCOVER
        if any(k in binding_lower for k in _PRINT_MEDIA_KEYWORDS_PAPERBACK):
            return cls.PAPERBACK
        if "ebook" in binding_lower or "e-book" in binding_lower:
            return cls.EBOOK

        return cls.UNKNOWN

    @property
    def is_audiobook(self) -> bool:
        """Whether this binding format represents an audiobook."""
        return self is BindingFormat.AUDIOBOOK

    @property
    def is_kindle(self) -> bool:
        """Whether this binding format represents a Kindle Edition."""
        return self is BindingFormat.KINDLE

    @property
    def is_paperback(self) -> bool:
        """Whether this binding format represents a Paperback."""
        return self is BindingFormat.PAPERBACK

    @property
    def is_hardcover(self) -> bool:
        """Whether this binding format represents a Hardcover."""
        return self is BindingFormat.HARDCOVER

    @property
    def is_ebook(self) -> bool:
        """Whether this binding format represents a Ebook."""
        return self is BindingFormat.EBOOK
