# 🗓️ Nepali Date Picker

A modern, production-ready date picker for Nepali (Bikram Sambat) and Gregorian calendars. Beautiful, accessible, and easy to use.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.2.5-green.svg)]()
[![](https://data.jsdelivr.com/v1/package/npm/@4mritgiri/npdatetime/badge)](https://www.jsdelivr.com/package/npm/@4mritgiri/npdatetime)

## ✨ Features

- 🎨 **Modern Design** - Beautiful glassmorphism UI with smooth animations
- 🕒 **Integrated Time Picker** - Select hours and minutes alongside dates
- ⚡ **Quick Actions** - "Today", "Yesterday", and "Tomorrow" shortcuts
- 📅 **Dual Calendar** - Seamlessly switch between Bikram Sambat (BS) and Gregorian (AD)
- 🌐 **Multi-language** - Full English & Nepali (Devanagari) support
- ♿ **Accessible** - Full keyboard navigation & ARIA support
- 📱 **Responsive** - Modal "bottom sheet" layout for mobile devices
- 📍 **Smart Positioning** - Follows input on scroll and window resize
- 📍 **Smart Input** - Auto-formatting `YYYY-MM-DD` masking and validation
- 🔢 **Keyboard Navigation** - Increment/decrement date segments with Arrow keys
- 🔒 **Strict Validation** - Prevents invalid characters and format errors
- 🟥 **Holiday Highlighting** - Saturdays (BS) and Sundays (AD) in red
- 🌙 **Dark Mode** - Automatic system theme integration
- 🏢 **Enterprise Options** - Disable past dates, weekends, holidays, specific dates/weekdays, and custom callbacks
- 🌙 **Tithi on Hover** - Show lunar tithi (Nepali date detail) on date hover
- 🎯 **Admin Theme** - Built-in Django admin theme integration
- 🚀 **Zero Dependencies** - Pure JavaScript and high-performance WASM
- ⚡ **Auto-Init** - Initialize via `type="npdate"` or `data-npdate`

## 🚀 Quick Start

### Installation
 
#### Via NPM (Recommended)
 
```bash
npm install @4mritgiri/npdatetime
```

#### Via CDN

You can use the library directly via CDN without installing:

```html
<!-- CSS -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@4mritgiri/npdatetime@0.2.5/picker.css">

<!-- JS Module -->
<script type="module">
  import NepaliDatePicker from 'https://cdn.jsdelivr.net/npm/@4mritgiri/npdatetime@0.2.5/picker.js';
  
  // Auto-initialize inputs
  NepaliDatePicker.init();
</script>
```
 
#### Manual Installation
 
1. Copy the following files to your project:
   - `picker.js`
   - `picker.css`
   - `pkg/` directory (WASM files)

2. Include in your HTML:

```html
<link rel="stylesheet" href="picker.css">
<script type="module">
  import NepaliDatePicker from './picker.js';
</script>
```

### Basic Usage

#### Automatic Initialization

Simply add `type="npdate"` or `data-npdate` to your inputs:

```html
<!-- Nepali Date (BS) -->
<input type="npdate" data-mode="BS" data-language="en">

<!-- With Nepali numerals -->
<input type="npdate" data-mode="BS" data-language="np">

<!-- Gregorian Date (AD) -->
<input type="npdate" data-mode="AD">
```

The library will automatically initialize all inputs on page load!

#### Manual Initialization

```javascript
import NepaliDatePicker from './picker.js';

// Create instance
const picker = new NepaliDatePicker('#my-input', {
  mode: 'BS',
  language: 'en',
  onChange: (date, picker) => {
    console.log('Selected:', date.format('%Y-%m-%d'));
  }
});

// Or initialize all npdate inputs manually
NepaliDatePicker.init();
```

## 📖 API Reference

### Constructor

```javascript
new NepaliDatePicker(element, options)
```

**Parameters:**
- `element` (string | HTMLElement) - CSS selector or DOM element
- `options` (object) - Configuration options

### Options

#### Core Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `mode` | string | `'BS'` | Calendar mode: `'BS'` or `'AD'` |
| `language` | string | `'en'` | Display language: `'en'` or `'np'` |
| `format` | string | `'%Y-%m-%d'` | Date format string |
| `minDate` | string | `null` | Minimum selectable date (YYYY-MM-DD) |
| `maxDate` | string | `null` | Maximum selectable date (YYYY-MM-DD) |
| `theme` | string | `'auto'` | Theme: `'auto'`, `'light'`, `'dark'`, or `'admin'` |
| `position` | string | `'auto'` | Picker position: `'auto'`, `'top'`, `'bottom'` |
| `closeOnSelect` | boolean | `true` | Close picker after selection |
| `showTodayButton` | boolean | `true` | Show "Today" button |
| `showClearButton` | boolean | `true` | Show "Clear" button |
| `onChange` | function | `null` | Callback when date changes |
| `onOpen` | function | `null` | Callback when picker opens |
| `onClose` | function | `null` | Callback when picker closes |

#### Dynamic Disabling Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `disabledDates` | array | `[]` | Array of date strings to disable (YYYY-MM-DD) |
| `disabledDays` | array | `[]` | Weekday indices to disable (0=Sun, 1=Mon, ..., 6=Sat) |
| `disablePastDates` | boolean | `false` | Disable all dates before today |
| `disableWeekends` | boolean | `false` | Disable weekends (Saturday in BS, Sunday in AD) |
| `disableHolidays` | boolean | `false` | Disable dates in `disabledDates` that are holidays |
| `holidayNames` | object | `{}` | Map of date strings to holiday names for tooltips |
| `onDateDisabled` | string | `'prevent'` | Behavior when disabled date is clicked: `'prevent'` or `'warn'` |
| `showTithi` | boolean | `false` | Show lunar tithi on date hover |

### Methods

```javascript
// Open the picker
picker.open();

// Close the picker
picker.close();

// Select today's date
picker.selectToday();

// Clear the selection
picker.clear();

// Switch calendar mode
picker.switchMode('BS' | 'AD');

// Destroy the picker (frees WASM memory)
picker.destroy();

// Get selected date
const date = picker.selectedDate; // Returns NepaliDate instance
```

### Static Methods

```javascript
// Initialize all npdate inputs
NepaliDatePicker.init(selector?, options?);

// Get instance from element
const picker = NepaliDatePicker.instances.get(element);
```

## 🎨 Customization

### Themes

The date picker comes with multiple color themes:

```html
<input type="npdate" data-theme="purple">
<input type="npdate" data-theme="green">
<input type="npdate" data-theme="orange">
<input type="npdate" data-theme="red">
```

### Django Admin Theme

Use the built-in admin theme to match Django admin styling:

```javascript
const picker = new NepaliDatePicker('#admin-date', {
  theme: 'admin',
});
```

Or via data attribute:

```html
<input type="npdate" data-theme="admin">
```

The admin theme uses Django admin's color palette (#417690 primary, #ba2121 danger) and adapts to the admin's font stack.

### Custom Styling

You can easily override CSS variables:

```css
:root {
  --npd-primary: #your-color;
  --npd-primary-hover: #your-hover-color;
  --npd-radius: 1rem;
}
```

### Dark Mode

Dark mode is automatically supported via `prefers-color-scheme` or you can force it:

```html
<html data-theme="dark">
```

## 📋 Examples

### Enterprise: Disable Past Dates & Weekends

```javascript
const picker = new NepaliDatePicker('#leave-date', {
  mode: 'BS',
  disablePastDates: true,
  disableWeekends: true,
  onChange: (date) => {
    console.log('Selected:', date.format('%Y-%m-%d'));
  }
});
```

### Disable Specific Dates & Days

```javascript
const picker = new NepaliDatePicker('#date-input', {
  mode: 'BS',
  disabledDates: ['2082-01-15', '2082-06-20'],  // Specific dates
  disabledDays: [0, 6],  // Disable Sundays & Saturdays
  onChange: (date) => {
    console.log('Selected:', date.format('%Y-%m-%d'));
  }
});
```

### Holidays with Tooltips

```javascript
const picker = new NepaliDatePicker('#date-input', {
  mode: 'BS',
  disabledDates: ['2082-01-01', '2082-08-10'],
  holidayNames: {
    '2082-01-01': 'New Year',
    '2082-08-10': 'Vijaya Dashami',
  },
  disableHolidays: true,
  onChange: (date) => {
    console.log('Selected:', date.format('%Y-%m-%d'));
  }
});
```

### With Validation

```javascript
const picker = new NepaliDatePicker('#date-input', {
  mode: 'BS',
  minDate: '2080-01-01',
  maxDate: '2085-12-30',
  onChange: (date) => {
    if (date) {
      console.log('Valid date selected:', date.format('%d %B %Y'));
    }
  }
});
```

### Show Tithi on Hover

```javascript
const picker = new NepaliDatePicker('#date-input', {
  mode: 'BS',
  showTithi: true,
  onChange: (date) => {
    console.log('Selected:', date.format('%Y-%m-%d'));
  }
});
```

### With Custom Format

```javascript
const picker = new NepaliDatePicker('#date-input', {
  mode: 'BS',
  format: '%d/%m/%Y', // DD/MM/YYYY format
  onChange: (date) => {
    console.log('Formatted:', date.format('%d %B %Y'));
  }
});
```

### Nepali Language

```javascript
const picker = new NepaliDatePicker('#date-input', {
  mode: 'BS',
  language: 'np', // Devanagari numerals
  onChange: (date) => {
    console.log('नेपाली मिति:', date.formatUnicode());
  }
});
```

### React Integration

**Note:** The picker automatically handles input masking and validation. Use the `onChange` callback to get the selected `NepaliDate` object.

```jsx
import { useEffect, useRef } from 'react';
import NepaliDatePicker from '@4mritgiri/npdatetime'; // or './picker.js'
import '@4mritgiri/npdatetime/picker.css'; // or './picker.css'

function DateInput() {
  const inputRef = useRef(null);
  const pickerRef = useRef(null);

  useEffect(() => {
    if (inputRef.current) {
      pickerRef.current = new NepaliDatePicker(inputRef.current, {
        mode: 'BS',
        disablePastDates: true,
        onChange: (date) => {
          console.log('Selected:', date);
        }
      });
    }

    return () => {
      pickerRef.current?.destroy();
    };
  }, []);

  return <input ref={inputRef} type="text" placeholder="YYYY-MM-DD" />;
}
```

### Vanilla JS (No Build Tools)

If you are not using a bundler (like Webpack or Vite), you can use valid ES Modules directly in the browser:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="./picker.css">
</head>
<body>
    <input type="text" id="my-date">

    <script type="module">
        import NepaliDatePicker from './picker.js';

        const picker = new NepaliDatePicker('#my-date');
    </script>
</body>
</html>
```
*Ensure `picker.js`, `picker.css`, and the `pkg/` folder are in the same directory.*

## ⚡ WASM Memory Management

This library uses WebAssembly for high-performance Nepali date calculations. `NepaliDate` objects allocate WASM linear memory that must be explicitly freed. The picker handles this internally, but if you create `NepaliDate` instances yourself, you **must** call `.free()` when done:

```javascript
import { NepaliDate } from './pkg/npdatetime.js';

// ✅ Correct: free after use
const date = new NepaliDate(2082, 1, 15);
console.log(date.format('%Y-%m-%d'));
date.free();

// ❌ Wrong: memory leak — WASM memory is never reclaimed
function leak() {
  const date = new NepaliDate(2082, 1, 15);
  return date.format('%Y-%m-%d');
  // date.free() never called — WASM memory grows unbounded
}
```

**Important:** JavaScript's `FinalizationRegistry` only triggers on GC, not on WASM memory pressure. In hot paths (e.g., rendering 42 days per month), always free immediately after use.

The picker's `destroy()` method frees all internal WASM objects. Always call `destroy()` when removing a picker instance:

```javascript
// Clean up on component unmount
picker.destroy();
```

## ⌨️ Keyboard Navigation

- **Enter/Space** - Open picker
- **Escape** - Close picker
- **Arrow Left** - Previous month
- **Arrow Right** - Next month
- **Tab** - Navigate through buttons

## 🌐 Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Opera (latest)

**Note:** WebAssembly support required

## 📦 File Structure

```
@4mritgiri/npdatetime/
├── picker.js        # Main library
├── picker.css       # Styles
├── pkg/                  # WASM bindings
│   ├── npdatetime.js
│   ├── npdatetime_bg.wasm
│   └── ...
├── demo/
│   └── index.html        # Demo page
└── README.md
```

## 🔧 Development

### Building from Source

```bash
# Install Rust and wasm-pack
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
cargo install wasm-pack

# Build WASM
cd bindings/javascript
wasm-pack build --target web

# Test
python -m http.server 8000
# Open http://localhost:8000/demo/
```

## 📝 Format Strings

The date picker supports the following format strings:

| Code | Description | Example |
|------|-------------|---------|
| `%Y` | 4-digit year | 2081 |
| `%m` | 2-digit month | 05 |
| `%d` | 2-digit day | 19 |
| `%B` | Full month name | Bhadra |
| `%b` | Short month name | Bha |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [npdatetime](https://github.com/4mritGiri/npdatetime)
- Inspired by modern date picker libraries

## 📞 Support

- 🐛 [Report Bug](https://github.com/4mritGiri/npdatetime/issues)
- 💡 [Request Feature](https://github.com/4mritGiri/npdatetime/issues)
- 📧 Email: amritgiri.dev@gmail.com

## 🗺️ Roadmap

- [x] Time picker support
- [x] Date range selection
- [x] NPM package
- [x] CDN hosting
- [x] Enterprise options (disable past dates, weekends, holidays)
- [x] Django admin theme
- [x] Tithi on hover
- [ ] More themes
- [ ] Mobile-optimized touch interactions

---

Made with ❤️ for Nepal
