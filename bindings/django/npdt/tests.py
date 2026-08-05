"""Tests for npdt widgets, forms, models, and holiday providers."""

import json

from django.test import TestCase, override_settings

from npdt.forms import NepaliDateField, NepaliDateRangeField, NepaliDateTimeField
from npdt.holidays import (
    CompositeHolidayProvider,
    HolidayDate,
    HolidayProvider,
    NepalPublicHolidays,
    StaticHolidayProvider,
)
from npdt.models import NepaliDateField as NepaliDateModelField
from npdt.widgets import (
    NepaliDatePickerWidget,
    NepaliDateRangeWidget,
    _normalize_disabled_days,
)


class NormalizeDisabledDaysTest(TestCase):
    """Test _normalize_disabled_days helper."""

    def test_list_of_ints(self):
        self.assertEqual(_normalize_disabled_days([0, 6]), [0, 6])

    def test_tuple(self):
        self.assertEqual(_normalize_disabled_days((0, 6)), [0, 6])

    def test_comma_separated_string(self):
        self.assertEqual(_normalize_disabled_days("0,6"), [0, 6])

    def test_range_string(self):
        self.assertEqual(_normalize_disabled_days("1-5"), [1, 2, 3, 4, 5])

    def test_mixed_string(self):
        self.assertEqual(_normalize_disabled_days("1-5,0"), [1, 2, 3, 4, 5, 0])

    def test_none(self):
        self.assertEqual(_normalize_disabled_days(None), [])

    def test_empty_string(self):
        self.assertEqual(_normalize_disabled_days(""), [])

    def test_empty_list(self):
        self.assertEqual(_normalize_disabled_days([]), [])

    def test_single_day_string(self):
        self.assertEqual(_normalize_disabled_days("6"), [6])

    def test_weekends_only(self):
        self.assertEqual(_normalize_disabled_days("0,6"), [0, 6])

    def test_monday_to_friday(self):
        self.assertEqual(_normalize_disabled_days("1-5"), [1, 2, 3, 4, 5])


class NepaliDatePickerWidgetTest(TestCase):
    """Test NepaliDatePickerWidget."""

    def test_basic_render(self):
        widget = NepaliDatePickerWidget()
        html = widget.render("test_date", None, attrs={})
        self.assertIn('name="test_date"', html)
        self.assertIn("npd-input", html)

    def test_mode_bs(self):
        widget = NepaliDatePickerWidget(mode="BS")
        html = widget.render("test_date", None, attrs={})
        self.assertIn('data-mode="BS"', html)

    def test_mode_ad(self):
        widget = NepaliDatePickerWidget(mode="AD")
        html = widget.render("test_date", None, attrs={})
        self.assertIn('data-mode="AD"', html)

    def test_language_np(self):
        widget = NepaliDatePickerWidget(language="np")
        html = widget.render("test_date", None, attrs={})
        self.assertIn('data-language="np"', html)

    def test_admin_theme(self):
        widget = NepaliDatePickerWidget(admin_theme=True)
        html = widget.render("test_date", None, attrs={})
        self.assertIn('data-theme="admin"', html)

    def test_disable_past_dates(self):
        widget = NepaliDatePickerWidget(disable_past_dates=True)
        html = widget.render("test_date", None, attrs={})
        self.assertIn("disablePastDates", html)

    def test_disable_weekends(self):
        widget = NepaliDatePickerWidget(disable_weekends=True)
        html = widget.render("test_date", None, attrs={})
        self.assertIn("disableWeekends", html)

    def test_disabled_days_list(self):
        widget = NepaliDatePickerWidget(disabled_days=[0, 6])
        context = widget.get_context("test_date", None, {})
        options = json.loads(context["widget"]["picker_options"])
        self.assertEqual(options["disabledDays"], [0, 6])

    def test_disabled_days_range_string(self):
        widget = NepaliDatePickerWidget(disabled_days="1-5")
        context = widget.get_context("test_date", None, {})
        options = json.loads(context["widget"]["picker_options"])
        self.assertEqual(options["disabledDays"], [1, 2, 3, 4, 5])

    def test_disabled_days_mixed_string(self):
        widget = NepaliDatePickerWidget(disabled_days="1-5,0")
        context = widget.get_context("test_date", None, {})
        options = json.loads(context["widget"]["picker_options"])
        self.assertEqual(options["disabledDays"], [1, 2, 3, 4, 5, 0])

    def test_disabled_dates(self):
        widget = NepaliDatePickerWidget(disabled_dates=["2082-01-01", "2082-09-03"])
        context = widget.get_context("test_date", None, {})
        options = json.loads(context["widget"]["picker_options"])
        self.assertIn("2082-01-01", options["disabledDates"])
        self.assertIn("2082-09-03", options["disabledDates"])

    def test_min_max_date(self):
        widget = NepaliDatePickerWidget(min_date="2082-01-01", max_date="2082-12-30")
        context = widget.get_context("test_date", None, {})
        options = json.loads(context["widget"]["picker_options"])
        self.assertEqual(options["minDate"], "2082-01-01")
        self.assertEqual(options["maxDate"], "2082-12-30")

    def test_media_css_js(self):
        widget = NepaliDatePickerWidget()
        self.assertIn("npdt/css/picker.css", str(widget.media))
        self.assertIn("npdt/js/picker.min.js", str(widget.media))

    def test_value_render(self):
        widget = NepaliDatePickerWidget()
        html = widget.render("test_date", "2082-01-15", attrs={})
        self.assertIn('value="2082-01-15"', html)

    def test_show_tithi(self):
        widget = NepaliDatePickerWidget(show_tithi=True)
        context = widget.get_context("test_date", None, {})
        options = json.loads(context["widget"]["picker_options"])
        self.assertTrue(options["showTithi"])

    def test_show_tithi_default(self):
        widget = NepaliDatePickerWidget()
        context = widget.get_context("test_date", None, {})
        options = json.loads(context["widget"]["picker_options"])
        self.assertNotIn("showTithi", options)


class NepaliDateRangeWidgetTest(TestCase):
    """Test NepaliDateRangeWidget."""

    def test_decompress_none(self):
        widget = NepaliDateRangeWidget()
        self.assertEqual(widget.decompress(None), [None, None])

    def test_decompress_range(self):
        widget = NepaliDateRangeWidget()
        self.assertEqual(
            widget.decompress("2082-01-01 to 2082-01-15"), ["2082-01-01", "2082-01-15"]
        )

    def test_decompress_single(self):
        widget = NepaliDateRangeWidget()
        self.assertEqual(widget.decompress("2082-01-01"), ["2082-01-01", ""])


class HolidayProviderTest(TestCase):
    """Test holiday provider system."""

    def test_nepal_public_holidays(self):
        provider = NepalPublicHolidays()
        holidays = provider.get_holidays(2082)
        self.assertTrue(len(holidays) > 0)
        # New Year should always be present
        dates = [h.date for h in holidays]
        self.assertIn("2082-01-01", dates)

    def test_nepal_public_holidays_by_month(self):
        provider = NepalPublicHolidays()
        holidays = provider.get_holidays(2082, month=1)
        for h in holidays:
            self.assertTrue(h.date.startswith("2082-01-"))

    def test_holiday_is_holiday(self):
        provider = NepalPublicHolidays()
        result = provider.is_holiday("2082-01-01")
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "New Year")

    def test_holiday_not_holiday(self):
        provider = NepalPublicHolidays()
        result = provider.is_holiday("2082-02-10")
        self.assertIsNone(result)

    def test_static_provider(self):
        provider = StaticHolidayProvider(
            ["2082-01-01", "2082-06-20"], name="Test Holiday"
        )
        holidays = provider.get_holidays(2082)
        self.assertEqual(len(holidays), 2)
        self.assertEqual(holidays[0].name, "Test Holiday")

    def test_composite_provider(self):
        p1 = StaticHolidayProvider(["2082-01-01"], name="H1")
        p2 = StaticHolidayProvider(["2082-01-01", "2082-06-20"], name="H2")
        composite = CompositeHolidayProvider(p1, p2)
        holidays = composite.get_holidays(2082)
        # Dedup: 2082-01-01 should appear only once
        dates = [h.date for h in holidays]
        self.assertEqual(len(dates), len(set(dates)))

    def test_holiday_date_equality(self):
        h1 = HolidayDate("2082-01-01", "New Year")
        h2 = HolidayDate("2082-01-01", "Different Name")
        self.assertEqual(h1, h2)

    def test_holiday_date_hash(self):
        h1 = HolidayDate("2082-01-01", "New Year")
        h2 = HolidayDate("2082-01-01", "Different Name")
        self.assertEqual(hash(h1), hash(h2))


class NepaliDateFieldFormTest(TestCase):
    """Test NepaliDateField form field."""

    def test_valid_bs_date(self):
        field = NepaliDateField(mode="BS")
        cleaned = field.clean("2082-01-15")
        self.assertEqual(cleaned, "2082-01-15")

    def test_invalid_format(self):
        field = NepaliDateField(mode="BS")
        from django.core.exceptions import ValidationError

        with self.assertRaises(ValidationError):
            field.clean("not-a-date")

    def test_widget_kwargs(self):
        field = NepaliDateField(
            widget_kwargs={
                "disable_past_dates": True,
                "admin_theme": True,
            }
        )
        self.assertIsInstance(field.widget, NepaliDatePickerWidget)

    def test_empty_required(self):
        field = NepaliDateField(required=True)
        from django.core.exceptions import ValidationError

        with self.assertRaises(ValidationError):
            field.clean("")

    def test_empty_optional(self):
        field = NepaliDateField(required=False)
        cleaned = field.clean("")
        self.assertEqual(cleaned, "")


class NepaliDateModelFieldTest(TestCase):
    """Test NepaliDateField model field."""

    def test_widget_kwargs_deconstruct(self):
        field = NepaliDateModelField(widget_kwargs={"disable_past_dates": True})
        name, path, args, kwargs = field.deconstruct()
        self.assertIn("widget_kwargs", kwargs)
        self.assertEqual(kwargs["widget_kwargs"], {"disable_past_dates": True})

    def test_default_deconstruct(self):
        field = NepaliDateModelField()
        name, path, args, kwargs = field.deconstruct()
        self.assertNotIn("widget_kwargs", kwargs)


class ValidateDateTest(TestCase):
    """Test NepaliDatePickerWidget.validate_date server-side validation."""

    def test_valid_date_passes(self):
        widget = NepaliDatePickerWidget(disable_weekends=True)
        # Should not raise — a weekday is fine
        widget.validate_date("2082-01-14")  # Tuesday in BS

    def test_disabled_date_rejected(self):
        widget = NepaliDatePickerWidget(disabled_dates=["2082-01-15"])
        from django.core.exceptions import ValidationError

        with self.assertRaises(ValidationError) as ctx:
            widget.validate_date("2082-01-15")
        self.assertEqual(ctx.exception.code, "disabled_date")

    def test_disabled_weekday_rejected(self):
        widget = NepaliDatePickerWidget(disabled_days=[0, 6])
        # Find a known Sunday — 2025-01-05 is a Sunday
        from django.core.exceptions import ValidationError

        widget_ad = NepaliDatePickerWidget(mode="AD", disabled_days=[0])
        with self.assertRaises(ValidationError) as ctx:
            widget_ad.validate_date("2025-01-05")
        self.assertEqual(ctx.exception.code, "disabled_weekday")

    def test_weekend_bs_rejected(self):
        widget = NepaliDatePickerWidget(mode="BS", disable_weekends=True)
        from django.core.exceptions import ValidationError

        # 2082-01-06 is a Saturday in BS
        with self.assertRaises(ValidationError) as ctx:
            widget.validate_date("2082-01-06")
        self.assertEqual(ctx.exception.code, "disabled_weekend")

    def test_weekend_ad_rejected(self):
        widget = NepaliDatePickerWidget(mode="AD", disable_weekends=True)
        from django.core.exceptions import ValidationError

        # 2025-01-05 is a Sunday
        with self.assertRaises(ValidationError) as ctx:
            widget.validate_date("2025-01-05")
        self.assertEqual(ctx.exception.code, "disabled_weekend")

    def test_past_date_rejected(self):
        widget = NepaliDatePickerWidget(mode="AD", disable_past_dates=True)
        from django.core.exceptions import ValidationError

        with self.assertRaises(ValidationError) as ctx:
            widget.validate_date("2020-01-01")
        self.assertEqual(ctx.exception.code, "past_date")

    def test_min_date_rejected(self):
        widget = NepaliDatePickerWidget(min_date="2082-06-01")
        from django.core.exceptions import ValidationError

        with self.assertRaises(ValidationError) as ctx:
            widget.validate_date("2082-05-15")
        self.assertEqual(ctx.exception.code, "min_date")

    def test_max_date_rejected(self):
        widget = NepaliDatePickerWidget(max_date="2082-06-01")
        from django.core.exceptions import ValidationError

        with self.assertRaises(ValidationError) as ctx:
            widget.validate_date("2082-06-15")
        self.assertEqual(ctx.exception.code, "max_date")

    def test_holiday_rejected(self):
        widget = NepaliDatePickerWidget(disable_holidays=True)
        from django.core.exceptions import ValidationError

        # New Year is always a holiday: 2082-01-01
        with self.assertRaises(ValidationError) as ctx:
            widget.validate_date("2082-01-01")
        self.assertEqual(ctx.exception.code, "holiday_date")

    def test_empty_value_passes(self):
        widget = NepaliDatePickerWidget(disable_weekends=True)
        # Should not raise for empty
        widget.validate_date("")
        widget.validate_date(None)
