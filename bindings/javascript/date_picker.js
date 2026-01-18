import init, { NepaliDate } from "./pkg/npdatetime_wasm.js";

export class NepaliDatePicker {
  static initialized = false;
  static instances = new Map();

  constructor(element, options = {}) {
    if (typeof element === "string") {
      element = document.querySelector(element);
    }

    if (!element) {
      throw new Error("Invalid element provided to NepaliDatePicker");
    }

    this.input = element;
    this.id = `npd-${Math.random().toString(36).substr(2, 9)}`;

    this.options = {
      mode: (element.dataset.mode || options.mode || "BS").toUpperCase(),
      language: (
        element.dataset.language ||
        options.language ||
        "en"
      ).toLowerCase(),
      format: options.format || "%Y-%m-%d",
      minDate: options.minDate || null,
      maxDate: options.maxDate || null,
      disabledDates: options.disabledDates || [],
      theme: element.dataset.theme || options.theme || "auto",
      position: options.position || "auto",
      closeOnSelect: options.closeOnSelect !== false,
      showTodayButton: options.showTodayButton !== false,
      showClearButton: options.showClearButton !== false,
      onChange: options.onChange || null,
      onOpen: options.onOpen || null,
      onClose: options.onClose || null,
      ...options,
    };

    this.selectedDate = null;
    this.selectedTime = {
      hour: options.defaultHour || 0,
      minute: options.defaultMinute || 0,
    };
    this.viewDate = { year: 2081, month: 1 };
    this.viewMode = "days";
    this.isOpen = false;

    this.init();
    NepaliDatePicker.instances.set(element, this);
  }

  async init() {
    if (!NepaliDatePicker.initialized) {
      await init();
      NepaliDatePicker.initialized = true;
    }

    this.setupInput();
    this.createPicker();
    this.attachEvents();
    this.parseInitialValue();

    if (!this.selectedDate) {
      this.setDetailsFromToday();
    }
  }

  setupInput() {
    this.input.setAttribute("autocomplete", "off");
    this.input.setAttribute("data-npd-id", this.id);
    this.input.classList.add("npd-input");

    if (!this.input.placeholder) {
      this.input.placeholder =
        this.options.mode === "BS" ? "Select Nepali Date" : "Select Date";
    }
  }

  createPicker() {
    const picker = document.createElement("div");
    picker.className = "npd-picker";
    picker.id = this.id;
    picker.setAttribute("role", "dialog");
    picker.setAttribute("aria-modal", "true");
    picker.innerHTML = `
      <div class="npd-header">
        <button type="button" class="npd-title" aria-label="Change view">
          <span class="npd-title-text"></span>
          <svg class="npd-title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="6 9 12 15 18 9"></polyline>
          </svg>
        </button>
        <div class="npd-nav">
          <button type="button" class="npd-nav-btn npd-prev" aria-label="Previous">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="15 18 9 12 15 6"></polyline>
            </svg>
          </button>
          <button type="button" class="npd-nav-btn npd-next" aria-label="Next">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </button>
        </div>
      </div>
      
      <div class="npd-body">
        <div class="npd-view npd-view-days"></div>
        <div class="npd-view npd-view-months"></div>
        <div class="npd-view npd-view-years"></div>
      </div>
      
      <div class="npd-footer">
        <div class="npd-mode-toggle">
          <button type="button" class="npd-mode-btn ${this.options.mode === "BS" ? "active" : ""}" data-mode="BS">
            <span>BS</span>
          </button>
          <button type="button" class="npd-mode-btn ${this.options.mode === "AD" ? "active" : ""}" data-mode="AD">
            <span>AD</span>
          </button>
        </div>
        <div class="npd-actions">
          ${this.options.showClearButton ? '<button type="button" class="npd-btn npd-clear">Clear</button>' : ""}
          <button type="button" class="npd-btn npd-yesterday">Yesterday</button>
          ${this.options.showTodayButton ? '<button type="button" class="npd-btn npd-today">Today</button>' : ""}
          <button type="button" class="npd-btn npd-tomorrow">Tomorrow</button>
        </div>

        <div class="npd-time-picker">
          <div class="npd-time-field">
            <label>Time</label>
            <div class="npd-time-inputs">
              <input type="number" class="npd-time-input npd-hour" min="0" max="23" value="${this.selectedTime.hour}" placeholder="HH">
              <span>:</span>
              <input type="number" class="npd-time-input npd-minute" min="0" max="59" value="${this.selectedTime.minute}" placeholder="mm">
            </div>
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(picker);
    this.picker = picker;
    this.elements = {
      title: picker.querySelector(".npd-title-text"),
      daysView: picker.querySelector(".npd-view-days"),
      monthsView: picker.querySelector(".npd-view-months"),
      yearsView: picker.querySelector(".npd-view-years"),
    };
  }

  attachEvents() {
    this.input.addEventListener("focus", () => this.open());
    this.input.addEventListener("click", () => this.open());
    this.input.addEventListener("keydown", (e) => this.handleInputKeydown(e));

    this.picker
      .querySelector(".npd-title")
      .addEventListener("click", () => this.changeViewMode());
    this.picker
      .querySelector(".npd-prev")
      .addEventListener("click", () => this.navigate(-1));
    this.picker
      .querySelector(".npd-next")
      .addEventListener("click", () => this.navigate(1));

    this.picker.querySelectorAll(".npd-mode-btn").forEach((btn) => {
      btn.addEventListener("click", () => this.switchMode(btn.dataset.mode));
    });

    if (this.options.showTodayButton) {
      this.picker
        .querySelector(".npd-today")
        .addEventListener("click", () => this.selectToday());
    }

    if (this.options.showClearButton) {
      this.picker
        .querySelector(".npd-clear")
        .addEventListener("click", () => this.clear());
    }

    this.picker
      .querySelector(".npd-yesterday")
      .addEventListener("click", () => this.selectYesterday());
    this.picker
      .querySelector(".npd-tomorrow")
      .addEventListener("click", () => this.selectTomorrow());

    this.picker.querySelector(".npd-hour").addEventListener("change", (e) => {
      this.selectedTime.hour = parseInt(e.target.value) || 0;
      this.updateInput();
    });

    this.picker.querySelector(".npd-minute").addEventListener("change", (e) => {
      this.selectedTime.minute = parseInt(e.target.value) || 0;
      this.updateInput();
    });

    document.addEventListener("click", (e) => {
      if (!this.picker.contains(e.target) && e.target !== this.input) {
        this.close();
      }
    });

    window.addEventListener("resize", () => {
      if (this.isOpen) this.position();
    });

    window.addEventListener(
      "scroll",
      () => {
        if (this.isOpen) this.position();
      },
      true,
    );
  }

  handleInputKeydown(e) {
    if (e.key === "Escape") {
      this.close();
    } else if (e.key === "Enter") {
      e.preventDefault();
      this.open();
    }
  }

  parseInitialValue() {
    const value = this.input.value.trim();
    if (!value) return;

    try {
      if (this.options.mode === "BS") {
        const [y, m, d] = value.split("-").map(Number);
        this.selectedDate = new NepaliDate(y, m, d);
      } else {
        const [y, m, d] = value.split("-").map(Number);
        this.selectedDate = NepaliDate.fromGregorian(y, m, d);
      }
      this.viewDate = {
        year: this.selectedDate.year,
        month: this.selectedDate.month,
      };
    } catch (e) {
      console.warn("Invalid initial date value:", value);
    }
  }

  setDetailsFromToday() {
    try {
      const today = NepaliDate.today();
      if (this.options.mode === "BS") {
        this.viewDate = { year: today.year, month: today.month };
      } else {
        const [y, m] = today.toGregorian();
        this.viewDate = { year: y, month: m };
      }
    } catch (e) {
      console.error("Failed to set default today date:", e);
    }
  }

  open() {
    if (this.isOpen) return;

    this.isOpen = true;
    this.picker.classList.add("active");
    this.position();
    this.render();

    if (this.options.onOpen) {
      this.options.onOpen(this);
    }
  }

  close() {
    if (!this.isOpen) return;

    this.isOpen = false;
    this.picker.classList.remove("active");

    if (this.options.onClose) {
      this.options.onClose(this);
    }
  }

  position() {
    const inputRect = this.input.getBoundingClientRect();
    const pickerHeight = 400;
    const spaceBelow = window.innerHeight - inputRect.bottom;
    const spaceAbove = inputRect.top;

    this.picker.style.left = `${inputRect.left}px`;
    this.picker.style.width = `${Math.max(inputRect.width, 320)}px`;

    if (
      this.options.position === "top" ||
      (this.options.position === "auto" &&
        spaceBelow < pickerHeight &&
        spaceAbove > spaceBelow)
    ) {
      this.picker.style.bottom = `${window.innerHeight - inputRect.top + 8}px`;
      this.picker.style.top = "auto";
      this.picker.classList.add("npd-position-top");
    } else {
      this.picker.style.top = `${inputRect.bottom + 8}px`;
      this.picker.style.bottom = "auto";
      this.picker.classList.remove("npd-position-top");
    }
  }

  switchMode(mode) {
    if (this.options.mode === mode) return;

    this.options.mode = mode;
    this.picker.querySelectorAll(".npd-mode-btn").forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.mode === mode);
    });

    if (this.selectedDate) {
      if (mode === "AD") {
        const [y, m] = this.selectedDate.toGregorian();
        this.viewDate = { year: y, month: m };
      } else {
        this.viewDate = {
          year: this.selectedDate.year,
          month: this.selectedDate.month,
        };
      }
    } else {
      // If no date is selected, convert the current view date
      try {
        if (mode === "AD") {
          // BS -> AD: Use Day 15 to avoid backward drift (Day 1 usually maps to previous month)
          const bsDate = new NepaliDate(
            this.viewDate.year,
            this.viewDate.month,
            15,
          );
          const [y, m] = bsDate.toGregorian();
          this.viewDate = { year: y, month: m };
        } else {
          // AD -> BS: Use Day 15
          const bsDate = NepaliDate.fromGregorian(
            this.viewDate.year,
            this.viewDate.month,
            15,
          );
          this.viewDate = { year: bsDate.year, month: bsDate.month };
        }
      } catch (e) {
        console.error("Failed to convert view date on mode switch:", e);
        this.setDetailsFromToday();
      }
    }

    this.render();
  }

  changeViewMode() {
    const modes = ["days", "months", "years"];
    const currentIndex = modes.indexOf(this.viewMode);
    this.viewMode = modes[(currentIndex + 1) % modes.length];
    this.render();
  }

  navigate(direction) {
    if (this.viewMode === "days") {
      this.viewDate.month += direction;
      if (this.viewDate.month > 12) {
        this.viewDate.month = 1;
        this.viewDate.year++;
      } else if (this.viewDate.month < 1) {
        this.viewDate.month = 12;
        this.viewDate.year--;
      }
    } else if (this.viewMode === "months") {
      this.viewDate.year += direction;
    } else {
      this.viewDate.year += direction * 12;
    }
    this.render();
  }

  render() {
    this.picker
      .querySelectorAll(".npd-view")
      .forEach((v) => v.classList.remove("active"));

    if (this.viewMode === "days") {
      this.renderDays();
    } else if (this.viewMode === "months") {
      this.renderMonths();
    } else {
      this.renderYears();
    }
  }

  renderDays() {
    const months =
      this.options.language === "np"
        ? [
            "बैशाख",
            "जेठ",
            "असार",
            "साउन",
            "भदौ",
            "असोज",
            "कात्तिक",
            "मंसिर",
            "पुस",
            "माघ",
            "फागुन",
            "चैत",
          ]
        : [
            "Baisakh",
            "Jestha",
            "Ashadh",
            "Shrawan",
            "Bhadra",
            "Ashwin",
            "Kartik",
            "Mangshir",
            "Poush",
            "Magh",
            "Falgun",
            "Chaitra",
          ];

    const weekdays =
      this.options.language === "np"
        ? ["आइत", "सोम", "मंगल", "बुध", "बिहि", "शुक्र", "शनि"]
        : ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

    if (this.options.mode === "BS") {
      const year =
        this.options.language === "np"
          ? this.toNepaliNum(this.viewDate.year)
          : this.viewDate.year;
      this.elements.title.textContent = `${months[this.viewDate.month - 1]} ${year}`;
    } else {
      const date = new Date(this.viewDate.year, this.viewDate.month - 1);
      this.elements.title.textContent = date.toLocaleDateString("en-US", {
        month: "long",
        year: "numeric",
      });
    }

    let html = '<div class="npd-days-grid">';
    weekdays.forEach((day) => {
      html += `<div class="npd-weekday">${day}</div>`;
    });

    if (this.options.mode === "BS") {
      const firstDate = new NepaliDate(
        this.viewDate.year,
        this.viewDate.month,
        1,
      );
      const [gy, gm, gd] = firstDate.toGregorian();
      const startWeekday = new Date(gy, gm - 1, gd).getDay();
      const daysInMonth = this.getDaysInMonth(
        this.viewDate.year,
        this.viewDate.month,
      );

      const prevMonth =
        this.viewDate.month === 1 ? 12 : this.viewDate.month - 1;
      const prevYear =
        this.viewDate.month === 1 ? this.viewDate.year - 1 : this.viewDate.year;
      const daysInPrevMonth = this.getDaysInMonth(prevYear, prevMonth);

      for (let i = startWeekday - 1; i >= 0; i--) {
        const day = daysInPrevMonth - i;
        const dayText =
          this.options.language === "np" ? this.toNepaliNum(day) : day;
        html += `<button type="button" class="npd-day npd-overflow" data-day="${day}" data-month-offset="-1">${dayText}</button>`;
      }

      const todayBS = NepaliDate.today();
      const isCurrentYear = this.viewDate.year === todayBS.year;
      const isCurrentMonth = this.viewDate.month === todayBS.month;

      for (let day = 1; day <= daysInMonth; day++) {
        const isSelected =
          this.selectedDate?.year === this.viewDate.year &&
          this.selectedDate?.month === this.viewDate.month &&
          this.selectedDate?.day === day;

        const isToday = isCurrentYear && isCurrentMonth && day === todayBS.day;

        const currentWeekday = (startWeekday + day - 1) % 7;
        const isHoliday = currentWeekday === 6; // Saturday in Nepal

        const dayText =
          this.options.language === "np" ? this.toNepaliNum(day) : day;
        html += `<button type="button" class="npd-day ${isSelected ? "selected" : ""} ${isToday ? "today" : ""} ${isHoliday ? "holiday" : ""}" data-day="${day}" data-month-offset="0">${dayText}</button>`;
      }

      // Next month overflow
      const totalCells = 42;
      const currentCells = startWeekday + daysInMonth;
      for (let day = 1; day <= totalCells - currentCells; day++) {
        const dayText =
          this.options.language === "np" ? this.toNepaliNum(day) : day;
        html += `<button type="button" class="npd-day npd-overflow" data-day="${day}" data-month-offset="1">${dayText}</button>`;
      }
    } else {
      const date = new Date(this.viewDate.year, this.viewDate.month - 1, 1);
      const startWeekday = date.getDay();
      const daysInMonth = new Date(
        this.viewDate.year,
        this.viewDate.month,
        0,
      ).getDate();

      const daysInPrevMonth = new Date(
        this.viewDate.year,
        this.viewDate.month - 1,
        0,
      ).getDate();

      for (let i = startWeekday - 1; i >= 0; i--) {
        const day = daysInPrevMonth - i;
        html += `<button type="button" class="npd-day npd-overflow" data-day="${day}" data-month-offset="-1">${day}</button>`;
      }

      const [selY, selM, selD] = this.selectedDate
        ? this.selectedDate.toGregorian()
        : [null, null, null];

      const today = new Date();
      const isCurrentYear = this.viewDate.year === today.getFullYear();
      const isCurrentMonth = this.viewDate.month === today.getMonth() + 1;

      for (let day = 1; day <= daysInMonth; day++) {
        const isSelected =
          selY === this.viewDate.year &&
          selM === this.viewDate.month &&
          selD === day;

        const isToday =
          isCurrentYear && isCurrentMonth && day === today.getDate();

        const currentWeekday = (startWeekday + day - 1) % 7;
        const isHoliday = currentWeekday === 0; // Sunday for AD

        html += `<button type="button" class="npd-day ${isSelected ? "selected" : ""} ${isToday ? "today" : ""} ${isHoliday ? "holiday" : ""}" data-day="${day}" data-month-offset="0">${day}</button>`;
      }

      // Next month overflow
      const totalCells = 42;
      const currentCells = startWeekday + daysInMonth;
      for (let day = 1; day <= totalCells - currentCells; day++) {
        html += `<button type="button" class="npd-day npd-overflow" data-day="${day}" data-month-offset="1">${day}</button>`;
      }
    }

    html += "</div>";
    this.elements.daysView.innerHTML = html;
    this.elements.daysView.classList.add("active");

    this.elements.daysView
      .querySelectorAll(".npd-day[data-day]")
      .forEach((btn) => {
        btn.addEventListener("click", (e) => {
          e.stopPropagation();
          const day = parseInt(btn.dataset.day);
          const offset = parseInt(btn.dataset.monthOffset || "0");

          if (offset !== 0) {
            let newMonth = this.viewDate.month + offset;
            let newYear = this.viewDate.year;

            if (newMonth > 12) {
              newMonth = 1;
              newYear++;
            } else if (newMonth < 1) {
              newMonth = 12;
              newYear--;
            }

            this.viewDate = { year: newYear, month: newMonth };
            this.render();
          } else {
            this.selectDate(day);
          }
        });
      });
  }

  renderMonths() {
    const months =
      this.options.language === "np"
        ? [
            "बैशाख",
            "जेठ",
            "असार",
            "साउन",
            "भदौ",
            "असोज",
            "कात्तिक",
            "मंसिर",
            "पुस",
            "माघ",
            "फागुन",
            "चैत",
          ]
        : [
            "Baisakh",
            "Jestha",
            "Ashadh",
            "Shrawan",
            "Bhadra",
            "Ashwin",
            "Kartik",
            "Mangshir",
            "Poush",
            "Magh",
            "Falgun",
            "Chaitra",
          ];

    const year =
      this.options.language === "np"
        ? this.toNepaliNum(this.viewDate.year)
        : this.viewDate.year;
    this.elements.title.textContent = year;

    let html = '<div class="npd-months-grid">';
    months.forEach((month, index) => {
      const isSelected =
        this.selectedDate?.year === this.viewDate.year &&
        this.selectedDate?.month === index + 1;
      html += `<button type="button" class="npd-month ${isSelected ? "selected" : ""}" data-month="${index + 1}">${month}</button>`;
    });
    html += "</div>";

    this.elements.monthsView.innerHTML = html;
    this.elements.monthsView.classList.add("active");

    this.elements.monthsView.querySelectorAll(".npd-month").forEach((btn) => {
      btn.addEventListener("click", () => {
        this.viewDate.month = parseInt(btn.dataset.month);
        this.viewMode = "days";
        this.render();
      });
    });
  }

  renderYears() {
    const startYear = Math.floor(this.viewDate.year / 12) * 12;
    this.elements.title.textContent = `${startYear} - ${startYear + 11}`;

    let html = '<div class="npd-years-grid">';
    for (let i = 0; i < 12; i++) {
      const year = startYear + i;
      const isSelected = this.selectedDate?.year === year;
      const yearText =
        this.options.language === "np" ? this.toNepaliNum(year) : year;
      html += `<button type="button" class="npd-year ${isSelected ? "selected" : ""}" data-year="${year}">${yearText}</button>`;
    }
    html += "</div>";

    this.elements.yearsView.innerHTML = html;
    this.elements.yearsView.classList.add("active");

    this.elements.yearsView.querySelectorAll(".npd-year").forEach((btn) => {
      btn.addEventListener("click", () => {
        this.viewDate.year = parseInt(btn.dataset.year);
        this.viewMode = "months";
        this.render();
      });
    });
  }

  selectDate(day) {
    try {
      if (this.options.mode === "BS") {
        this.selectedDate = new NepaliDate(
          this.viewDate.year,
          this.viewDate.month,
          day,
        );
      } else {
        this.selectedDate = NepaliDate.fromGregorian(
          this.viewDate.year,
          this.viewDate.month,
          day,
        );
      }

      this.updateInput();
      if (this.options.closeOnSelect) {
        this.close();
      } else {
        this.render();
      }

      if (this.options.onChange) {
        this.options.onChange(this.selectedDate, this);
      }
    } catch (e) {
      console.error("Invalid date selection:", e);
    }
  }

  selectToday() {
    this.selectedDate = NepaliDate.today();
    this.viewDate = {
      year: this.selectedDate.year,
      month: this.selectedDate.month,
    };
    this.updateInput();
    this.close();

    if (this.options.onChange) {
      this.options.onChange(this.selectedDate, this);
    }
  }

  selectYesterday() {
    const today = NepaliDate.today();
    this.selectedDate = today.addDays(-1);
    this.viewDate = {
      year: this.selectedDate.year,
      month: this.selectedDate.month,
    };
    this.updateInput();
    this.close();

    if (this.options.onChange) {
      this.options.onChange(this.selectedDate, this);
    }
  }

  selectTomorrow() {
    const today = NepaliDate.today();
    this.selectedDate = today.addDays(1);
    this.viewDate = {
      year: this.selectedDate.year,
      month: this.selectedDate.month,
    };
    this.updateInput();
    this.close();

    if (this.options.onChange) {
      this.options.onChange(this.selectedDate, this);
    }
  }

  clear() {
    this.selectedDate = null;
    this.input.value = "";
    this.close();

    if (this.options.onChange) {
      this.options.onChange(null, this);
    }
  }

  updateInput() {
    if (!this.selectedDate) {
      this.input.value = "";
      return;
    }

    if (this.options.mode === "BS") {
      let value = this.selectedDate.format(this.options.format);
      if (
        this.options.format.includes("%H") ||
        this.options.format.includes("%M") ||
        true
      ) {
        // Simple append if not in format (or we can enhance format support in WASM but let's do JS side for now)
        const timeStr = `${String(this.selectedTime.hour).padStart(2, "0")}:${String(this.selectedTime.minute).padStart(2, "0")}`;
        if (!value.includes(":")) value += ` ${timeStr}`;
      }
      this.input.value = value;
    } else {
      const [y, m, d] = this.selectedDate.toGregorian();
      this.input.value = `${y}-${String(m).padStart(2, "0")}-${String(d).padStart(2, "0")} ${String(this.selectedTime.hour).padStart(2, "0")}:${String(this.selectedTime.minute).padStart(2, "0")}`;
    }

    this.input.dispatchEvent(new Event("change", { bubbles: true }));
  }

  getDaysInMonth(year, month) {
    try {
      for (let d = 32; d >= 27; d--) {
        try {
          new NepaliDate(year, month, d);
          return d;
        } catch (e) {}
      }
    } catch (e) {}
    return 30;
  }

  toNepaliNum(num) {
    const map = ["०", "१", "२", "३", "४", "५", "६", "७", "८", "९"];
    return String(num).replace(/\d/g, (d) => map[+d]);
  }

  destroy() {
    this.close();
    this.picker.remove();
    this.input.classList.remove("npd-input");
    this.input.removeAttribute("data-npd-id");
    NepaliDatePicker.instances.delete(this.input);
  }

  static init(
    selector = 'input[type="npdate"], input[data-npdate]',
    options = {},
  ) {
    const inputs = document.querySelectorAll(selector);
    inputs.forEach((input) => {
      if (!NepaliDatePicker.instances.has(input)) {
        new NepaliDatePicker(input, options);
      }
    });
  }
}

if (typeof document !== "undefined") {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () =>
      NepaliDatePicker.init(),
    );
  } else {
    NepaliDatePicker.init();
  }
}

export default NepaliDatePicker;
