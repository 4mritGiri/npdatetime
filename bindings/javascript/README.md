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

## Building

```bash
# For bundlers (default)
npm run build

# For Node.js
npm run build:nodejs

# For web (no bundler)
npm run build:web
```

## Features

- ⚡ **Blazing Fast**: Near-native performance via WebAssembly
- 🎯 **Accurate**: Verified against official BS calendar data (1975-2100)
- 📦 **Tiny**: ~50KB WASM binary (gzipped)
- 🔧 **Type-Safe**: Full TypeScript definitions included
- 🌐 **Universal**: Works in browsers, Node.js, and Deno

## License

MIT
