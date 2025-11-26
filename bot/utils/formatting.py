"""
Formatting utilities for visual enhancements in bot messages.
"""


def format_progress_bar(value: float, max_value: float = 1.0, length: int = 10) -> str:
    """
    Create visual progress bar.

    Args:
        value: Current value (e.g., confidence 0.94)
        max_value: Maximum value (usually 1.0)
        length: Bar length in characters

    Returns:
        Progress bar string like "█████████░ 94%"

    Example:
        >>> format_progress_bar(0.94)
        '█████████░ 94%'
    """
    if value < 0:
        value = 0
    if value > max_value:
        value = max_value

    percentage = (value / max_value) * 100
    filled = int((value / max_value) * length)
    empty = length - filled

    bar = "█" * filled + "░" * empty
    return f"{bar} {percentage:.0f}%"


def format_water_urgency_visual(urgency: str) -> str:
    """
    Visual representation of urgency with colored circles.

    Args:
        urgency: Urgency level ("low", "medium", "high", "critical")

    Returns:
        Visual indicator string

    Example:
        >>> format_water_urgency_visual("critical")
        '🔴🔴🔴🔴🔴'
    """
    urgency_map = {
        "low": "🟢" + "⚪" * 4,
        "medium": "🟡" * 3 + "⚪" * 2,
        "high": "🟠" * 4 + "⚪",
        "critical": "🔴" * 5
    }
    return urgency_map.get(urgency, "⚪" * 5)


def format_large_number(num: int) -> str:
    """
    Format large numbers with spaces (Russian/Kyrgyz style).

    Args:
        num: Number to format

    Returns:
        Formatted number string

    Example:
        >>> format_large_number(12450)
        '12 450'
    """
    return f"{num:,}".replace(",", " ")


def format_confidence_level(confidence: float) -> str:
    """
    Get textual confidence level description.

    Args:
        confidence: Confidence value (0.0 to 1.0)

    Returns:
        Confidence level description

    Example:
        >>> format_confidence_level(0.95)
        'Очень высокая'
    """
    if confidence >= 0.9:
        return "Очень высокая ✅"
    elif confidence >= 0.7:
        return "Высокая ✅"
    elif confidence >= 0.5:
        return "Средняя ⚠️"
    else:
        return "Низкая ❌"
