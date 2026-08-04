"""Holiday provider system for Nepali date picker.

Provides an extensible framework for defining which dates should be
treated as holidays in the date picker widget. Includes built-in
Nepal public holiday support and a base class for custom providers.
"""

from abc import ABC, abstractmethod
from datetime import date


class HolidayProvider(ABC):
    """Base class for holiday providers.

    Subclass this to define custom holiday logic for your organization.
    The provider is called by the widget to determine which dates are
    holidays and should be disabled/highlighted in the picker.

    Example::

        class MyCompanyHolidays(HolidayProvider):
            def get_holidays(self, year, month=None):
                return [
                    HolidayDate('2082-01-01', 'Company Foundation Day'),
                    HolidayDate('2082-06-15', 'Annual Retreat'),
                ]
    """

    @abstractmethod
    def get_holidays(self, year, month=None):
        """Return holidays for the given year, optionally filtered by month.

        Args:
            year (int): The year to get holidays for.
            month (int, optional): If provided, only return holidays
                for this month (1-12).

        Returns:
            list[HolidayDate]: List of holidays for the requested period.
        """
        raise NotImplementedError

    def is_holiday(self, date_str):
        """Check if a specific date is a holiday.

        Default implementation iterates get_holidays(). Override for
        better performance if your provider has many holidays.

        Args:
            date_str (str): Date in YYYY-MM-DD format.

        Returns:
            HolidayDate or None: The holiday if found, else None.
        """
        try:
            parts = date_str.split("-")
            year = int(parts[0])
            month = int(parts[1]) if len(parts) > 1 else None
        except (ValueError, IndexError):
            return None

        for holiday in self.get_holidays(year, month):
            if holiday.date == date_str:
                return holiday
        return None


class HolidayDate:
    """A single holiday entry.

    Attributes:
        date (str): Date in YYYY-MM-DD format.
        name (str): Human-readable name of the holiday.
        name_np (str): Nepali name of the holiday (optional).
        type (str): Holiday type: 'public', 'bank', 'optional'.
    """

    __slots__ = ("date", "name", "name_np", "type")

    def __init__(self, date, name="", name_np="", type="public"):
        self.date = date
        self.name = name
        self.name_np = name_np
        self.type = type

    def __repr__(self):
        return f"HolidayDate({self.date!r}, {self.name!r})"

    def __eq__(self, other):
        if isinstance(other, HolidayDate):
            return self.date == other.date
        return NotImplemented

    def __hash__(self):
        return hash(self.date)


class NepalPublicHolidays(HolidayProvider):
    """Built-in Nepal public holiday provider.

    Covers major Nepali public holidays for BS years 2070-2100.
    These are the nationally observed holidays that fall on fixed
    dates each year in the Bikram Sambat calendar.

    Note: Some holidays (like Dashain/Tihar) shift slightly each year.
    This provider includes the commonly observed dates. For exact
    government calendar holidays, extend with a custom provider.
    """

    # Fixed BS-date holidays (month, day) -> (name_en, name_np)
    FIXED_HOLIDAYS = {
        (1, 1): ("New Year", "नयाँ वर्ष"),
        (1, 14): ("Labour Day", "श्रम दिवस"),
        (3, 15): ("Constitution Day", "संविधान दिवस"),
        (5, 1): ("Janai Purnima", "जनै पूर्णिमा"),
        (5, 15): ("Gai Jatra", "गाई जात्रा"),
        (6, 4): ("Krishna Janmashtami", "कृष्ण जन्माष्टमी"),
        (6, 19): ("Father's Day", "बुबा जन्मदिन"),
        (7, 1): ("Indra Jatra", "इन्द्र जात्रा"),
        (8, 1): ("Dashain (Ghatasthapana)", "दशैं (घटस्थापना)"),
        (8, 7): ("Phulpati", "फूलपाती"),
        (8, 8): ("Maha Ashtami", "महाष्टमी"),
        (8, 9): ("Maha Nawami", "महानवमी"),
        (8, 10): ("Vijaya Dashami", "विजया दशमी"),
        (8, 15): ("Kojagrat Purnima", "कोजाग्रत पूर्णिमा"),
        (9, 1): ("Tihar (Laxmi Puja)", "तिहार (लक्ष्मी पूजा)"),
        (9, 2): ("Tihar (Mha Puja)", "तिहार (म्ह पूजा)"),
        (9, 3): ("Tihar (Bhai Tika)", "तिहार (भाई टीका)"),
        (9, 5): ("Chhath", "छठ"),
        (10, 1): ("Nepal Sambat New Year", "नेपाल सम्बत नयाँ वर्ष"),
        (10, 15): ("Mother's Day", "आमा जन्मदिन"),
        (11, 15): ("Maghe Sankranti", "माघे सक्रान्ति"),
        (11, 29): ("Shivaratri", "शिवरात्रि"),
        (12, 8): ("Fagu Purnima (Holi)", "फागु पूर्णिमा (होली)"),
        (12, 15): ("Chaitra Dashain", "चैत्र दशैं"),
        (12, 29): ("Ram Nawami", "राम नवमी"),
    }

    def get_holidays(self, year, month=None):
        """Return Nepal public holidays for the given BS year.

        Args:
            year (int): BS year.
            month (int, optional): BS month (1-12).

        Returns:
            list[HolidayDate]: List of holidays.
        """
        holidays = []
        for (m, d), (name_en, name_np) in self.FIXED_HOLIDAYS.items():
            if month is not None and m != month:
                continue
            date_str = f"{year}-{m:02d}-{d:02d}"
            holidays.append(HolidayDate(date_str, name_en, name_np, "public"))
        return holidays


class CompositeHolidayProvider(HolidayProvider):
    """Combine multiple holiday providers.

    Useful when you want to merge Nepal public holidays with
    company-specific holidays.

    Example::

        provider = CompositeHolidayProvider(
            NepalPublicHolidays(),
            MyCompanyHolidays(),
        )
    """

    def __init__(self, *providers):
        self.providers = providers

    def get_holidays(self, year, month=None):
        seen = set()
        result = []
        for provider in self.providers:
            for holiday in provider.get_holidays(year, month):
                if holiday.date not in seen:
                    seen.add(holiday.date)
                    result.append(holiday)
        return result

    def is_holiday(self, date_str):
        for provider in self.providers:
            h = provider.is_holiday(date_str)
            if h:
                return h
        return None


class StaticHolidayProvider(HolidayProvider):
    """A simple provider backed by a list of date strings.

    Useful for quick one-off configurations without writing a full class.

    Example::

        provider = StaticHolidayProvider([
            '2082-01-01',
            '2082-09-03',
        ])
    """

    def __init__(self, dates, name=""):
        """
        Args:
            dates (list[str]): List of date strings in YYYY-MM-DD format.
            name (str): Optional name for all holidays in this set.
        """
        self.dates = dates
        self._name = name

    def get_holidays(self, year, month=None):
        result = []
        for d in self.dates:
            parts = d.split("-")
            y = int(parts[0])
            m = int(parts[1])
            if y == year and (month is None or m == month):
                result.append(HolidayDate(d, self._name))
        return result

    def is_holiday(self, date_str):
        if date_str in self.dates:
            return HolidayDate(date_str, self._name)
        return None
