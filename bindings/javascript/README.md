# 🗓️ Nepali Date Picker

A modern, production-ready date picker for Nepali (Bikram Sambat) and Gregorian calendars. Beautiful, accessible, and easy to use.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)]()

## ✨ Features

- 🎨 **Modern Design** - Beautiful glassmorphism UI with smooth animations
- 🕒 **Integrated Time Picker** - Select hours and minutes alongside dates
- ⚡ **Quick Actions** - "Today", "Yesterday", and "Tomorrow" shortcuts
- 📅 **Dual Calendar** - Seamlessly switch between Bikram Sambat (BS) and Gregorian (AD)
- 🌐 **Multi-language** - Full English & Nepali (Devanagari) support
- ♿ **Accessible** - Full keyboard navigation & ARIA support
- 📱 **Responsive** - Modal "bottom sheet" layout for mobile devices
- 📍 **Smart Positioning** - Follows input on scroll and window resize
- 🟥 **Holiday Highlighting** - Saturdays (BS) and Sundays (AD) in red
- 🌙 **Dark Mode** - Automatic system theme integration
- 🚀 **Zero Dependencies** - Pure JavaScript and high-performance WASM
- ⚡ **Auto-Init** - Initialize via `type="npdate"` or `data-npdate`

## 🚀 Quick Start

### Installation
 
#### Via NPM (Recommended)
 
```bash
npm install @4mritgiri/npdatetime
```
 
#### Manual Installation
 
1. Copy the following files to your project:
   - `date_picker.js`
   - `date_picker.css`
   - `pkg/` directory (WASM files)

2. Include in your HTML:

```html
<link rel="stylesheet" href="date_picker.css">
<script type="module">
  import NepaliDatePicker from './date_picker.js';
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
import NepaliDatePicker from './date_picker.js';

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

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `mode` | string | `'BS'` | Calendar mode: `'BS'` or `'AD'` |
| `language` | string | `'en'` | Display language: `'en'` or `'np'` |
| `format` | string | `'%Y-%m-%d'` | Date format string |
| `minDate` | NepaliDate | `null` | Minimum selectable date |
| `maxDate` | NepaliDate | `null` | Maximum selectable date |
| `disabledDates` | array | `[]` | Array of disabled dates |
| `theme` | string | `'auto'` | Theme: `'auto'`, `'light'`, `'dark'` |
| `position` | string | `'auto'` | Picker position: `'auto'`, `'top'`, `'bottom'` |
| `closeOnSelect` | boolean | `true` | Close picker after selection |
| `showTodayButton` | boolean | `true` | Show "Today" button |
| `showClearButton` | boolean | `true` | Show "Clear" button |
| `onChange` | function | `null` | Callback when date changes |
| `onOpen` | function | `null` | Callback when picker opens |
| `onClose` | function | `null` | Callback when picker closes |

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

// Destroy the picker
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

### With Validation

```javascript
const picker = new NepaliDatePicker('#date-input', {
  mode: 'BS',
  minDate: new NepaliDate(2080, 1, 1),
  maxDate: new NepaliDate(2081, 12, 30),
  onChange: (date) => {
    if (date) {
      console.log('Valid date selected:', date.format('%d %B %Y'));
    }
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

```jsx
import { useEffect, useRef } from 'react';
import NepaliDatePicker from './date_picker.js';

function DateInput() {
  const inputRef = useRef(null);
  const pickerRef = useRef(null);

  useEffect(() => {
    if (inputRef.current) {
      pickerRef.current = new NepaliDatePicker(inputRef.current, {
        mode: 'BS',
        onChange: (date) => {
          console.log('Selected:', date);
        }
      });
    }

    return () => {
      pickerRef.current?.destroy();
    };
  }, []);

  return <input ref={inputRef} type="text" />;
}
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
├── date_picker.js        # Main library
├── date_picker.css       # Styles
├── pkg/                  # WASM bindings
│   ├── npdatetime_wasm.js
│   ├── npdatetime_wasm_bg.wasm
│   └── ...
├── demo/
│   └── demo.html        # Demo page
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

- Built with [npdatetime-rust](https://github.com/your-repo/npdatetime-rust)
- Inspired by modern date picker libraries

## 📞 Support

- 🐛 [Report Bug](https://github.com/your-repo/issues)
- 💡 [Request Feature](https://github.com/your-repo/issues)
- 📧 Email: your-email@example.com

## 🗺️ Roadmap

- [ ] Time picker support
- [ ] Date range selection
- [ ] More themes
- [ ] Mobile-optimized touch interactions
- [x] NPM package
- [ ] CDN hosting

---

Made with ❤️ for Nepal
