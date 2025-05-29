import jdatetime


class JalaliDate:
    """
    A utility class for working with today's Jalali (Persian) date.

    Provides common string representations such as ISO format (YYYY-MM-DD)
    and a more readable format with Persian month names.

    Example usage:
        date = JalaliDate()
        print(date.iso())
        print(date.pretty())
    """

    def __init__(self):
        """
        Initializes the JalaliDate instance with today's Jalali date.
        """
        self.today: jdatetime.date = jdatetime.date.today()

    def iso(self) -> str:
        """
        Returns:
            str: The date in ISO format (e.g. 'yyyy-mm-dd').
        """
        return self.today.strftime("%Y-%m-%d")

    def pretty(self) -> str:
        """
        Returns:
            str: The date in a more readable format (e.g. 'yyyy month dd).
        """
        return self.today.strftime("%d %B %Y")
