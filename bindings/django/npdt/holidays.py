"""Holiday provider system for Nepali date picker.

Provides an extensible framework for defining which dates should be
treated as holidays in the date picker widget. Includes built-in
Nepal public holiday support and a base class for custom providers.
"""

from abc import ABC, abstractmethod


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
    """Built-in Nepal public holiday provider using astronomical Tithi calculations from npdatetime.

    Covers major Nepal public holidays dynamically based on astronomical Tithis
    and Bikram Sambat solar transits.
    """

    # Fixed solar BS-date holidays (month, day) -> (name_en, name_np)
    FIXED_HOLIDAYS = {
        (1, 1): ("New Year", "नयाँ वर्ष"),
        (1, 14): ("Labour Day", "श्रम दिवस"),
        (3, 15): ("Constitution Day", "संविधान दिवस"),
        (11, 1): ("Maghe Sankranti", "माघे सक्रान्ति"),
    }

    def get_holidays(self, year, month=None):
        """Return Nepal public holidays for the given BS year calculated dynamically via astronomical Tithis using npdatetime.

        Args:
            year (int): BS year.
            month (int, optional): BS month (1-12).

        Returns:
            list[HolidayDate]: List of holidays.
        """
        from npdatetime import NepaliDate

        months_to_check = [month] if month is not None else list(range(1, 13))
        holidays = []

        for m in months_to_check:
            try:
                start_bs = NepaliDate(year, m, 1)
            except Exception:
                continue

            curr_bs = start_bs
            while curr_bs.month == m:
                d = curr_bs.day
                date_str = f"{year}-{m:02d}-{d:02d}"

                if (m, d) in self.FIXED_HOLIDAYS:
                    name_en, name_np = self.FIXED_HOLIDAYS[(m, d)]
                    holidays.append(HolidayDate(date_str, name_en, name_np, "public"))

                # Use npdatetime library directly for astronomical Tithi details
                details = curr_bs.tithi_details()
                tithi_num = details["index"]
                is_shukla = (details["paksha"] == "Shukla")
                shukla_day = tithi_num if is_shukla else 0
                krishna_day = (tithi_num - 15) if not is_shukla else 0

                tithi_evts = []
                if m == 1 and shukla_day == 15:
                    tithi_evts.append(("Buddha Jayanti", "बुद्ध जयन्ती"))

                if m in (4, 5):
                    if shukla_day == 15:
                        tithi_evts.append(("Janai Purnima", "जनै पूर्णिमा"))
                    elif krishna_day == 1:
                        tithi_evts.append(("Gai Jatra", "गाई जात्रा"))

                if m == 5:
                    if shukla_day == 3:
                        tithi_evts.append(("Haritalika Teej", "हरितालिका तीज"))
                    elif shukla_day == 5:
                        tithi_evts.append(("Rishi Panchami", "ऋषि पञ्चमी"))
                    elif krishna_day == 8:
                        tithi_evts.append(("Krishna Janmashtami", "कृष्ण जन्माष्टमी"))
                    elif krishna_day == 15:
                        tithi_evts.append(("Kushe Aushi (Father's Day)", "कुशे औंशी (बुबाको मुख हेर्ने दिन)"))
                    elif shukla_day == 14:
                        tithi_evts.append(("Indra Jatra", "इन्द्र जात्रा"))

                if (m == 6 and shukla_day > 0) or (m == 7 and shukla_day > 0 and d < 15):
                    if shukla_day == 1:
                        tithi_evts.append(("Dashain (Ghatasthapana)", "दशैं (घटस्थापना)"))
                    elif shukla_day == 7:
                        tithi_evts.append(("Phulpati", "फूलपाती"))
                    elif shukla_day == 8:
                        tithi_evts.append(("Maha Ashtami", "महाष्टमी"))
                    elif shukla_day == 9:
                        tithi_evts.append(("Maha Nawami", "महानवमी"))
                    elif shukla_day == 10:
                        tithi_evts.append(("Vijaya Dashami", "विजया दशमी"))
                    elif shukla_day == 15:
                        tithi_evts.append(("Kojagrat Purnima", "कोजाग्रत पूर्णिमा"))

                if m == 7:
                    if krishna_day == 15:
                        tithi_evts.append(("Tihar (Laxmi Puja)", "तिहार (लक्ष्मी पूजा)"))
                    elif shukla_day == 1:
                        tithi_evts.append(("Tihar (Mha Puja)", "तिहार (म्ह पूजा)"))
                    elif shukla_day == 2:
                        tithi_evts.append(("Tihar (Bhai Tika)", "तिहार (भाई टीका)"))
                    elif shukla_day == 6:
                        tithi_evts.append(("Chhath", "छठ"))

                if m == 10 and shukla_day == 5:
                    tithi_evts.append(("Shree Panchami", "श्रीपञ्चमी (सरस्वती पूजा)"))

                if m == 11:
                    if krishna_day == 14:
                        tithi_evts.append(("Shivaratri", "शिवरात्रि"))
                    elif shukla_day == 15:
                        tithi_evts.append(("Fagu Purnima (Holi)", "फागु पूर्णिमा (होली)"))

                if m == 12:
                    if shukla_day == 8:
                        tithi_evts.append(("Chaitra Dashain", "चैत्र दशैं"))
                    elif shukla_day == 9:
                        tithi_evts.append(("Ram Nawami", "राम नवमी"))

                for name_en, name_np in tithi_evts:
                    holidays.append(HolidayDate(date_str, name_en, name_np, "public"))

                curr_bs = curr_bs.add_days(1)

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
