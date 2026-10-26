/* tslint:disable */
/* eslint-disable */

/**
 * Astronomical Bikram Sambat date for JavaScript
 */
export class BsDate {
    free(): void;
    [Symbol.dispose](): void;
    static fromGregorian(year: number, month: number, day: number): BsDate;
    /**
     * Create a new astronomical BS date
     */
    constructor(year: number, month: number, day: number);
    /**
     * Get Tithi for the date (Astronomical)
     */
    tithi(): string;
    toGregorian(): Int32Array;
    toString(): string;
    readonly day: number;
    readonly month: number;
    readonly year: number;
}

/**
 * Nepali (Bikram Sambat) date for JavaScript
 */
export class NepaliDate {
    free(): void;
    [Symbol.dispose](): void;
    /**
     * Add days to the date
     *
     * @param {number} days - Number of days to add (can be negative)
     * @returns {NepaliDate} New date after adding days
     */
    addDays(days: number): NepaliDate;
    /**
     * Format the date in Unicode Devanagari script
     */
    formatUnicode(): string;
    /**
     * Format the date as a string
     *
     * @param {string} format - Format string (strftime-style)
     * @returns {string} Formatted date string
     *
     * @example
     * const date = new NepaliDate(2077, 5, 19);
     * console.log(date.format("%d %B %Y")); // "19 Bhadra 2077"
     */
    format(format_str: string): string;
    /**
     * Create NepaliDate from Gregorian (AD) date
     *
     * @param {number} year - Gregorian year
     * @param {number} month - Month (1-12)
     * @param {number} day - Day of month
     * @returns {NepaliDate} Converted Nepali date
     *
     * @example
     * const date = NepaliDate.fromGregorian(2020, 9, 4);
     * console.log(date.toString()); // "2077-05-19"
     */
    static fromGregorian(year: number, month: number, day: number): NepaliDate;
    /**
     * Create NepaliDate from an ordinal
     */
    static fromOrdinal(ordinal: number): NepaliDate;
    /**
     * Generate a visual month calendar
     */
    monthCalendar(): string;
    /**
     * Create a new Nepali date
     *
     * @param {number} year - Bikram Sambat year
     * @param {number} month - Month (1-12)
     * @param {number} day - Day of month
     * @returns {NepaliDate} New NepaliDate instance
     *
     * @example
     * const date = new NepaliDate(2077, 5, 19);
     * console.log(date.toString()); // "2077-05-19"
     */
    constructor(year: number, month: number, day: number);
    /**
     * Get detailed Tithi information including start and end times in NPT
     */
    tithiDetails(): any;
    /**
     * Get Tithi for the date (Astronomical)
     *
     * @returns {string} Tithi name (e.g., "Shukla Pratipada")
     */
    tithi(): string;
    /**
     * Convert to Gregorian (AD) date
     *
     * @returns {Array<number>} [year, month, day]
     *
     * @example
     * const date = new NepaliDate(2077, 5, 19);
     * const [year, month, day] = date.toGregorian();
     * console.log(`${year}-${month}-${day}`); // "2020-9-4"
     */
    toGregorian(): Int32Array;
    /**
     * Get the ordinal representation of the date (days since 1975-01-01 BS)
     */
    toOrdinal(): number;
    /**
     * String representation
     */
    toString(): string;
    /**
     * Get today's Nepali date
     *
     * @returns {NepaliDate} Today's date in BS
     */
    static today(): NepaliDate;
    /**
     * Get the day
     */
    readonly day: number;
    /**
     * Get the fiscal quarter (1-4)
     */
    readonly fiscalQuarter: number;
    /**
     * Get the Nepali Fiscal Year (e.g., "2080/81")
     */
    readonly fiscalYear: string;
    /**
     * Get the month (1-12)
     */
    readonly month: number;
    /**
     * Get the year
     */
    readonly year: number;
}

/**
 * Initialize WASM module
 */
export function init(): void;

export type InitInput = RequestInfo | URL | Response | BufferSource | WebAssembly.Module;

export interface InitOutput {
    readonly memory: WebAssembly.Memory;
    readonly __wbg_bsdate_free: (a: number, b: number) => void;
    readonly __wbg_nepalidate_free: (a: number, b: number) => void;
    readonly bsdate_day: (a: number) => number;
    readonly bsdate_fromGregorian: (a: number, b: number, c: number, d: number) => void;
    readonly bsdate_month: (a: number) => number;
    readonly bsdate_new: (a: number, b: number, c: number, d: number) => void;
    readonly bsdate_tithi: (a: number, b: number) => void;
    readonly bsdate_toGregorian: (a: number, b: number) => void;
    readonly bsdate_toString: (a: number, b: number) => void;
    readonly bsdate_year: (a: number) => number;
    readonly init: () => void;
    readonly nepalidate_addDays: (a: number, b: number, c: number) => void;
    readonly nepalidate_day: (a: number) => number;
    readonly nepalidate_fiscalQuarter: (a: number) => number;
    readonly nepalidate_fiscalYear: (a: number, b: number) => void;
    readonly nepalidate_format: (a: number, b: number, c: number, d: number) => void;
    readonly nepalidate_formatUnicode: (a: number, b: number) => void;
    readonly nepalidate_fromGregorian: (a: number, b: number, c: number, d: number) => void;
    readonly nepalidate_fromOrdinal: (a: number, b: number) => void;
    readonly nepalidate_month: (a: number) => number;
    readonly nepalidate_monthCalendar: (a: number, b: number) => void;
    readonly nepalidate_new: (a: number, b: number, c: number, d: number) => void;
    readonly nepalidate_tithi: (a: number, b: number) => void;
    readonly nepalidate_tithiDetails: (a: number, b: number) => void;
    readonly nepalidate_toGregorian: (a: number, b: number) => void;
    readonly nepalidate_toOrdinal: (a: number) => number;
    readonly nepalidate_toString: (a: number, b: number) => void;
    readonly nepalidate_today: (a: number) => void;
    readonly nepalidate_year: (a: number) => number;
    readonly __wbindgen_export: (a: number, b: number) => number;
    readonly __wbindgen_export2: (a: number, b: number, c: number, d: number) => number;
    readonly __wbindgen_export3: (a: number, b: number, c: number) => void;
    readonly __wbindgen_add_to_stack_pointer: (a: number) => number;
    readonly __wbindgen_start: () => void;
}

export type SyncInitInput = BufferSource | WebAssembly.Module;

/**
 * Instantiates the given `module`, which can either be bytes or
 * a precompiled `WebAssembly.Module`.
 *
 * @param {{ module: SyncInitInput }} module - Passing `SyncInitInput` directly is deprecated.
 *
 * @returns {InitOutput}
 */
export function initSync(module: { module: SyncInitInput } | SyncInitInput): InitOutput;

/**
 * If `module_or_path` is {RequestInfo} or {URL}, makes a request and
 * for everything else, calls `WebAssembly.instantiate` directly.
 *
 * @param {{ module_or_path: InitInput | Promise<InitInput> }} module_or_path - Passing `InitInput` directly is deprecated.
 *
 * @returns {Promise<InitOutput>}
 */
export default function __wbg_init (module_or_path?: { module_or_path: InitInput | Promise<InitInput> } | InitInput | Promise<InitInput>): Promise<InitOutput>;
