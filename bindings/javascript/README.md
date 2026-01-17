# NPDateTime - WASM/JavaScript

Fast Nepali (Bikram Sambat) datetime library for JavaScript/TypeScript via WebAssembly.

## Installation

```bash
npm install npdatetime-wasm
```

## Quick Start

### For Bundlers (Webpack, Vite, etc.)

```javascript
import init, { NepaliDate } from 'npdatetime-wasm';

await init();

// Create a Nepali date
const date = new NepaliDate(2077, 5, 19);
console.log(date.toString()); // "2077-05-19"

// Convert to Gregorian
const [year, month, day] = date.toGregorian();
console.log(`${year}-${month}-${day}`); // "2020-9-4"

// Create from Gregorian
const bsDate = NepaliDate.fromGregorian(2020, 9, 4);
console.log(bsDate.toString()); // "2077-05-19"

// Get today's date
const today = NepaliDate.today();
console.log(today.toString());

// Format dates
const formatted = date.format("%d %B %Y");
console.log(formatted); // "19 Bhadra 2077"

// Date arithmetic
const future = date.addDays(30);
console.log(future.toString());

// Access properties
console.log(date.year);  // 2077
console.log(date.month); // 5
console.log(date.day);   // 19
```

### For Node.js

Build for Node.js target:
```bash
npm run build:nodejs
```

Then use:
```javascript
const { NepaliDate } = require('./pkg/npdatetime_wasm');

const date = new NepaliDate(2077, 5, 19);
console.log(date.toString());
```

## UI Components

### 📅 NepaliADDatePicker (v2.0)

A high-performance, premium standalone date picker component with zero external dependencies.

#### Features
- **Dual Mode**: Seamlessly switch between Bikram Sambat (BS) and Gregorian (AD).
- **Smart Positioning**: Automatically flips between Top/Bottom based on screen space.
- **Auto Theme**: Built-in light/dark mode support (follows system preferences).
- **Fast Navigation**: Year & Decade selection grids for rapid date hopping.
- **Accessibility**: Full keyboard navigation (Arrows, Enter, Escape).
- **Localized**: Complete Devanagari numerals and labels support.

#### Usage

```javascript
import { NepaliADDatePicker } from './date_picker.js';

const picker = new NepaliADDatePicker('picker-container', {
    mode: 'BS',        // Default 'BS'
    language: 'NP',    // 'NP' for Devanagari, 'EN' for English
    onSelect: (date) => {
        console.log("Selected Date:", date.format("%Y-%m-%d"));
    }
});
```

Include the styles in your HTML:
```html
<link rel="stylesheet" href="date_picker.css">
```

## Building

```bash
# Build WASM and JS packages
npm run build
```

## Features

- ⚡ **Blazing Fast**: Near-native performance via WebAssembly.
- 🎨 **Premium UI**: Glassmorphism design with fluid, bouncy animations.
- 🎯 **Accurate**: Verified against official BS calendar data (1975-2100).
- 📦 **Tiny**: Standalone component with small WASM footprint.
- 🔧 **Type-Safe**: Full TypeScript definitions included.

## License

MIT
