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

    this.init();
  }

  async init() {
    await init();
    this.selectedDate = NepaliDate.today();
    this.viewDate = {
      year: this.selectedDate.year,
      month: this.selectedDate.month,
    };
    this.initialized = true;
    this.renderBaseStructure();
    this.attachEvents();
    this.updateDisplay();
  }

  renderBaseStructure() {
    this.container.classList.add("np-datepicker-container");
    this.container.innerHTML = `
            <div class="np-datepicker-input-wrapper" id="dp-input">
                <span id="dp-display-value">Select Date</span>
                <span style="margin-left: auto;">📅</span>
            </div>
            <div class="np-datepicker-modal" id="dp-modal">
                <div class="np-datepicker-header">
                    <div class="np-datepicker-title" id="dp-month-year"></div>
                    <div class="np-datepicker-nav">
                        <button class="np-datepicker-nav-btn" id="dp-prev">◀</button>
                        <button class="np-datepicker-nav-btn" id="dp-next">▶</button>
                    </div>
                </div>
                <div class="np-datepicker-grid" id="dp-grid"></div>
                <div class="np-datepicker-switch">
                    <button class="np-datepicker-switch-btn ${this.options.mode === "BS" ? "active" : ""}" data-mode="BS">Bikram Sambat</button>
                    <button class="np-datepicker-switch-btn ${this.options.mode === "AD" ? "active" : ""}" data-mode="AD">Gregorian (AD)</button>
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

    this.container
      .querySelector("#dp-prev")
      .addEventListener("click", () => this.changeMonth(-1));
    this.container
      .querySelector("#dp-next")
      .addEventListener("click", () => this.changeMonth(1));

    this.container
      .querySelectorAll(".np-datepicker-switch-btn")
      .forEach((btn) => {
        btn.addEventListener("click", (e) =>
          this.switchMode(e.target.dataset.mode),
        );
      });

    // Close on click outside
    document.addEventListener("click", (e) => {
      if (!this.container.contains(e.target)) {
        this.closeModal();
      }
    });
  }

  toggleModal() {
    if (this.isOpen) this.closeModal();
    else this.openModal();
  }

  openModal() {
    this.modal.classList.add("active");
    this.isOpen = true;
    this.renderCalendar();
  }

  closeModal() {
    this.modal.classList.remove("active");
    this.isOpen = false;
  }

  switchMode(mode) {
    if (this.options.mode === mode) return;

    this.options.mode = mode;
    this.container
      .querySelectorAll(".np-datepicker-switch-btn")
      .forEach((btn) => {
        btn.classList.toggle("active", btn.dataset.mode === mode);
      });

    // When switching, update viewDate to match the current selectedDate in the new mode
    if (mode === "AD") {
      const [y, m, d] = this.selectedDate.toGregorian();
      this.viewDate = { year: y, month: m };
    } else {
      this.viewDate = {
        year: this.selectedDate.year,
        month: this.selectedDate.month,
      };
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

  renderCalendar() {
    this.grid.innerHTML = "";

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

  renderBSCalendar() {
    const monthNames = [
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
    this.monthYearTitle.textContent = `${monthNames[this.viewDate.month - 1]} ${this.viewDate.year}`;

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
      div.textContent = d;

      if (
        this.selectedDate.year === this.viewDate.year &&
        this.selectedDate.month === this.viewDate.month &&
        this.selectedDate.day === d
      ) {
        div.classList.add("selected");
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
    if (this.options.mode === "BS") {
      display.textContent = this.selectedDate.format("%d %B %Y");
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

  // Helper because the current bindings might not expose days_in_month directly easily or efficiently
  getBSDaysInMonth(y, m) {
    // We can just use the WASM instance to check
    try {
      // A simple way is to try creating a date with 32 and if it fails, try 31, then 30...
      // But actually we have a better way: NepaliDate.from_ordinal / to_ordinal logic internal
      // For now, let's use a simple binary search or just loop backwards from 32
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
