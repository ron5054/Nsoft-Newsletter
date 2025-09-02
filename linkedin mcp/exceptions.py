"""
Custom exceptions for LinkedIn post text extraction.
"""


class LinkedInExtractorError(Exception):
    """Base exception for LinkedIn extractor errors."""
    pass


class InvalidURLError(LinkedInExtractorError):
    """Raised when the provided URL is not a valid LinkedIn post URL."""
    pass


class ExtractionFailedError(LinkedInExtractorError):
    """Raised when text extraction fails."""
    pass


class PrivatePostError(LinkedInExtractorError):
    """Raised when attempting to access a private post."""
    pass


class NetworkError(LinkedInExtractorError):
    """Raised when network-related errors occur."""
    pass


class PlaywrightError(LinkedInExtractorError):
    """Raised when Playwright-related errors occur."""
    pass