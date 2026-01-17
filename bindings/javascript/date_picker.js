import init, { NepaliDate } from "./pkg/npdatetime_wasm.js";

export class NepaliADDatePicker {
  constructor(elementId, options = {}) {
    this.container = document.getElementById(elementId);
    this.options = {
      mode: "BS", // 'BS' or 'AD'
      language: "NP", // 'EN' or 'NP'
      onSelect: null,
      ...options,
    };

    this.isOpen = false;
    this.initialized = false;
    this.viewMode = "month"; // 'month' or 'year'

    this.init();
  }

  async init() {
    await init();
    this.selectedDate = NepaliDate.today();
    this.viewDate = {
      year: this.selectedDate.year,
      month: this.selectedDate.month,
    };
    this.viewYear = this.viewDate.year; // Base year for decade view
    this.initialized = true;
    this.renderBaseStructure();
    this.attachEvents();
    this.updateDisplay();
  }

  renderBaseStructure() {
    this.container.classList.add("np-datepicker-container");
    this.container.innerHTML = `
            <div class="np-datepicker-input-wrapper" id="dp-input" tabindex="0" role="button" aria-haspopup="true" aria-expanded="false">
                <span id="dp-display-value">Select Date</span>
                <span style="margin-left: auto; opacity: 0.6;">📅</span>
            </div>
            <div class="np-datepicker-modal" id="dp-modal" tabindex="-1">
                <div class="np-datepicker-header">
                    <div class="np-datepicker-title" id="dp-month-year" tabindex="0"></div>
                    <div class="np-datepicker-nav">
                        <button class="np-datepicker-nav-btn" id="dp-prev" title="Previous Month">◀</button>
                        <button class="np-datepicker-nav-btn" id="dp-next" title="Next Month">▶</button>
                    </div>
                </div>
                <div class="np-datepicker-grid" id="dp-grid" role="grid"></div>
                
                <div class="np-datepicker-switch">
                    <button class="np-datepicker-switch-btn ${this.options.mode === "BS" ? "active" : ""}" data-mode="BS">Bikram Sambat</button>
                    <button class="np-datepicker-switch-btn ${this.options.mode === "AD" ? "active" : ""}" data-mode="AD">Gregorian (AD)</button>
                </div>

                <div class="np-datepicker-footer">
                    <button class="np-datepicker-footer-btn" id="dp-clear">Clear</button>
                    <button class="np-datepicker-footer-btn primary" id="dp-today">Today</button>
                </div>
            </div>
        `;

    this.modal = this.container.querySelector("#dp-modal");
    this.inputWrapper = this.container.querySelector("#dp-input");
    this.grid = this.container.querySelector("#dp-grid");
    this.monthYearTitle = this.container.querySelector("#dp-month-year");
  }

  attachEvents() {
    this.inputWrapper.addEventListener("click", () => this.toggleModal());

    // Header click for year view toggle
    this.monthYearTitle.addEventListener("click", (e) => {
      e.stopPropagation();
      this.toggleViewMode();
    });

    // Month/Year Navigation
    this.container.querySelector("#dp-prev").addEventListener("click", (e) => {
      e.stopPropagation();
      if (this.viewMode === "month") {
        this.changeMonth(-1);
      } else {
        this.changeDecade(-1);
      }
    });
    this.container.querySelector("#dp-next").addEventListener("click", (e) => {
      e.stopPropagation();
      if (this.viewMode === "month") {
        this.changeMonth(1);
      } else {
        this.changeDecade(1);
      }
    });

    // Mode Switching
    this.container
      .querySelectorAll(".np-datepicker-switch-btn")
      .forEach((btn) => {
        btn.addEventListener("click", (e) => {
          e.stopPropagation();
          this.switchMode(e.target.dataset.mode);
        });
      });

    // Footer Buttons
    this.container.querySelector("#dp-today").addEventListener("click", (e) => {
      e.stopPropagation();
      this.selectedDate = NepaliDate.today();
      this.viewDate = {
        year: this.selectedDate.year,
        month: this.selectedDate.month,
      };
      if (this.options.mode === "AD") {
        const [y, m] = this.selectedDate.toGregorian();
        this.viewDate = { year: y, month: m };
      }
      this.updateDisplay();
      this.renderCalendar();
      this.closeModal();
      if (this.options.onSelect) this.options.onSelect(this.selectedDate);
    });

    this.container.querySelector("#dp-clear").addEventListener("click", (e) => {
      e.stopPropagation();
      const display = this.container.querySelector("#dp-display-value");
      display.textContent = "Select Date";
      this.closeModal();
      if (this.options.onSelect) this.options.onSelect(null);
    });

    // Keyboard Accessibility
    this.container.addEventListener("keydown", (e) => this.handleKeydown(e));

    // Close on click outside
    document.addEventListener("click", (e) => {
      if (!this.container.contains(e.target)) {
        this.closeModal();
      }
    });

    // Auto-reposition on scroll/resize if open
    window.addEventListener(
      "scroll",
      () => {
        if (this.isOpen) this.updatePosition();
      },
      true,
    );
    window.addEventListener("resize", () => {
      if (this.isOpen) this.updatePosition();
    });
  }

  handleKeydown(e) {
    if (!this.isOpen) {
      if (e.key === "Enter" || e.key === " ") {
        this.openModal();
        e.preventDefault();
      }
      return;
    }

    switch (e.key) {
      case "Escape":
        this.closeModal();
        break;
      case "ArrowLeft":
        this.changeMonth(-1);
        break;
      case "ArrowRight":
        this.changeMonth(1);
        break;
      case "Tab":
        // Let default tabbing work but keep focus in modal if needed (optional)
        break;
    }
  }

  updatePosition() {
    const rect = this.inputWrapper.getBoundingClientRect();
    const modalHeight = 400; // Estimated max height
    const spaceBelow = window.innerHeight - rect.bottom;
    const spaceAbove = rect.top;

    this.modal.classList.remove("pos-top", "pos-bottom");

    if (spaceBelow < modalHeight && spaceAbove > spaceBelow) {
      this.modal.classList.add("pos-top");
    } else {
      this.modal.classList.add("pos-bottom");
    }
  }

  toggleModal() {
    if (this.isOpen) this.closeModal();
    else this.openModal();
  }

  openModal() {
    this.updatePosition();
    this.modal.classList.add("active");
    this.isOpen = true;
    this.inputWrapper.setAttribute("aria-expanded", "true");
    this.renderCalendar();
  }

  closeModal() {
    this.modal.classList.remove("active");
    this.isOpen = false;
    this.inputWrapper.setAttribute("aria-expanded", "false");
  }

  switchMode(mode) {
    if (this.options.mode === mode) return;

    // Capture current view context to convert it
    const currentY = this.viewDate.year;
    const currentM = this.viewDate.month;

    this.options.mode = mode;
    this.container
      .querySelectorAll(".np-datepicker-switch-btn")
      .forEach((btn) => {
        btn.classList.toggle("active", btn.dataset.mode === mode);
      });

    // Smart synchronization of view context
    if (mode === "AD") {
      // Convert BS view context to AD
      try {
        const tempDate = new NepaliDate(currentY, currentM, 1);
        const [y, m] = tempDate.toGregorian();
        this.viewDate = { year: y, month: m };
      } catch (e) {
        // Fallback to selectedDate if current view is invalid for some reason
        const [y, m] = this.selectedDate.toGregorian();
        this.viewDate = { year: y, month: m };
      }
    } else {
      // Convert AD view context to BS
      try {
        const tempDate = NepaliDate.fromGregorian(currentY, currentM, 1);
        this.viewDate = { year: tempDate.year, month: tempDate.month };
      } catch (e) {
        this.viewDate = {
          year: this.selectedDate.year,
          month: this.selectedDate.month,
        };
      }
    }

    // If in year mode, sync viewYear as well
    if (this.viewMode === "year") {
      this.viewYear = this.viewDate.year;
    }

    this.renderCalendar();
    this.updateDisplay();
  }

  changeMonth(delta) {
    let newMonth = this.viewDate.month + delta;
    let newYear = this.viewDate.year;

    if (newMonth > 12) {
      newMonth = 1;
      newYear++;
    } else if (newMonth < 1) {
      newMonth = 12;
      newYear--;
    }
    this.viewDate = { year: newYear, month: newMonth };
    this.renderCalendar();
  }

  toggleViewMode() {
    this.viewMode = this.viewMode === "month" ? "year" : "month";
    if (this.viewMode === "year") {
      this.viewYear = this.viewDate.year;
    }
    this.renderCalendar();
  }

  changeDecade(delta) {
    this.viewYear += delta * 12; // Show 12 years in a 3x4 grid
    this.renderCalendar();
  }

  renderCalendar() {
    this.grid.innerHTML = "";

    if (this.viewMode === "year") {
      this.renderYearGrid();
      return;
    }

    // Ensure year grid class is removed when switching back to month view
    this.grid.classList.remove("np-datepicker-year-grid");

    const weekdaysEN = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"];
    const weekdaysNP = ["आइ", "सो", "मं", "बु", "बि", "शु", "श"];

    // Auto-switch weekday language for AD mode for better UX
    const useNP = this.options.mode === "BS" && this.options.language === "NP";
    const weekdays = useNP ? weekdaysNP : weekdaysEN;

    weekdays.forEach((wd) => {
      const div = document.createElement("div");
      div.className = "np-datepicker-weekday";
      div.textContent = wd;
      this.grid.appendChild(div);
    });

    if (this.options.mode === "BS") {
      this.renderBSCalendar();
    } else {
      this.renderADCalendar();
    }
  }

  renderYearGrid() {
    this.monthYearTitle.textContent = `${this.viewYear} - ${this.viewYear + 11}`;
    this.grid.classList.add("np-datepicker-year-grid");

    for (let i = 0; i < 12; i++) {
      const year = this.viewYear + i;
      const div = document.createElement("div");
      div.className = "np-datepicker-day np-datepicker-year";

      const useNP = this.options.language === "NP";
      div.textContent = useNP ? this.toDevanagari(year) : year;

      if (year === this.viewDate.year) {
        div.classList.add("selected");
      }

      div.addEventListener("click", (e) => {
        e.stopPropagation();
        this.selectYear(year);
      });
      this.grid.appendChild(div);
    }
  }

  selectYear(year) {
    this.viewDate.year = year;
    this.viewMode = "month";
    this.grid.classList.remove("np-datepicker-year-grid");
    this.renderCalendar();
  }

  renderBSCalendar() {
    const monthNamesEN = [
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
    const monthNamesNP = [
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
    ];

    const useNP = this.options.language === "NP";
    const monthNames = useNP ? monthNamesNP : monthNamesEN;

    const titleText = useNP
      ? `${monthNames[this.viewDate.month - 1]} ${this.toDevanagari(this.viewDate.year)}`
      : `${monthNames[this.viewDate.month - 1]} ${this.viewDate.year}`;

    this.monthYearTitle.textContent = titleText;

    const firstOfMonth = new NepaliDate(
      this.viewDate.year,
      this.viewDate.month,
      1,
    );
    const [gY, gM, gD] = firstOfMonth.toGregorian();
    const startWeekday = new Date(gY, gM - 1, gD).getDay();

    const daysInMonth = this.getBSDaysInMonth(
      this.viewDate.year,
      this.viewDate.month,
    );

    for (let i = 0; i < startWeekday; i++) {
      const div = document.createElement("div");
      div.className = "np-datepicker-day empty";
      this.grid.appendChild(div);
    }

    for (let d = 1; d <= daysInMonth; d++) {
      const div = document.createElement("div");
      div.className = "np-datepicker-day";

      const useNP = this.options.language === "NP";
      div.textContent = useNP ? this.toDevanagari(d) : d;
      div.setAttribute(
        "aria-label",
        `${d} ${monthNames[this.viewDate.month - 1]}`,
      );

      if (
        this.selectedDate.year === this.viewDate.year &&
        this.selectedDate.month === this.viewDate.month &&
        this.selectedDate.day === d
      ) {
        div.classList.add("selected");
        div.setAttribute("aria-selected", "true");
      }

      div.addEventListener("click", () => this.selectDateBS(d));
      this.grid.appendChild(div);
    }
  }

  renderADCalendar() {
    const date = new Date(this.viewDate.year, this.viewDate.month - 1, 1);
    const monthName = date.toLocaleString("default", { month: "long" });
    this.monthYearTitle.textContent = `${monthName} ${this.viewDate.year}`;

    const startWeekday = date.getDay();
    const daysInMonth = new Date(
      this.viewDate.year,
      this.viewDate.month,
      0,
    ).getDate();

    for (let i = 0; i < startWeekday; i++) {
      const div = document.createElement("div");
      div.className = "np-datepicker-day empty";
      this.grid.appendChild(div);
    }

    const [selY, selM, selD] = this.selectedDate.toGregorian();

    for (let d = 1; d <= daysInMonth; d++) {
      const div = document.createElement("div");
      div.className = "np-datepicker-day";
      div.textContent = d;

      if (
        selY === this.viewDate.year &&
        selM === this.viewDate.month &&
        selD === d
      ) {
        div.classList.add("selected");
      }

      div.addEventListener("click", () => this.selectDateAD(d));
      this.grid.appendChild(div);
    }
  }

  selectDateBS(day) {
    this.selectedDate = new NepaliDate(
      this.viewDate.year,
      this.viewDate.month,
      day,
    );
    this.updateDisplay();
    this.closeModal();
    if (this.options.onSelect) this.options.onSelect(this.selectedDate);
  }

  selectDateAD(day) {
    this.selectedDate = NepaliDate.fromGregorian(
      this.viewDate.year,
      this.viewDate.month,
      day,
    );
    this.updateDisplay();
    this.closeModal();
    if (this.options.onSelect) this.options.onSelect(this.selectedDate);
  }

  updateDisplay() {
    const display = this.container.querySelector("#dp-display-value");
    const useNP = this.options.language === "NP";

    if (this.options.mode === "BS") {
      let text = this.selectedDate.format("%d %B %Y");
      if (useNP) {
        // Localize month and numerals in display
        const monthNamesEN = [
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
        const monthNamesNP = [
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
        ];

        let [d, mStr, y] = text.split(" ");
        const mIndex = monthNamesEN.indexOf(mStr);
        const mNP = monthNamesNP[mIndex];
        text = `${this.toDevanagari(d)} ${mNP} ${this.toDevanagari(y)}`;
      }
      display.textContent = text;
    } else {
      const [y, m, d] = this.selectedDate.toGregorian();
      const date = new Date(y, m - 1, d);
      display.textContent = date.toLocaleDateString(undefined, {
        day: "numeric",
        month: "long",
        year: "numeric",
      });
    }
  }

  toDevanagari(num) {
    const devanagariMap = ["०", "१", "२", "३", "४", "५", "६", "७", "८", "९"];
    return String(num).replace(/[0-9]/g, (w) => devanagariMap[+w]);
  }

  // Helper because the current bindings might not expose days_in_month directly easily or efficiently
  getBSDaysInMonth(y, m) {
    // We can just use the WASM instance to check
    try {
      for (let d = 32; d >= 27; d--) {
        try {
          new NepaliDate(y, m, d);
          return d;
        } catch (e) {}
      }
    } catch (e) {}
    return 30;
  }
}
