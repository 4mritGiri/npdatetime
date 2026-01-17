use criterion::{BenchmarkId, Criterion, black_box, criterion_group, criterion_main};
use npdatetime::{NepaliDate, lookup};

fn bench_days_in_month(c: &mut Criterion) {
    let mut group = c.benchmark_group("days_in_month");

    // Benchmark lookup table access
    group.bench_function("lookup_2077_bhadra", |b| {
        b.iter(|| black_box(lookup::get_days_in_month(2077, 5)));
    });

    group.bench_function("lookup_first_year", |b| {
        b.iter(|| black_box(lookup::get_days_in_month(1975, 1)));
    });

    group.bench_function("lookup_last_year", |b| {
        b.iter(|| black_box(lookup::get_days_in_month(2100, 12)));
    });

    group.finish();
}

fn bench_date_creation(c: &mut Criterion) {
    c.bench_function("create_valid_date", |b| {
        b.iter(|| black_box(NepaliDate::new(2077, 5, 19)));
    });
}

fn bench_bs_to_ad_conversion(c: &mut Criterion) {
    let mut group = c.benchmark_group("bs_to_ad");

    let date = NepaliDate::new(2077, 5, 19).unwrap();

    group.bench_function("to_gregorian", |b| {
        b.iter(|| black_box(date.to_gregorian()));
    });

    group.finish();
}

fn bench_ad_to_bs_conversion(c: &mut Criterion) {
    c.bench_function("from_gregorian", |b| {
        b.iter(|| black_box(NepaliDate::from_gregorian(2020, 9, 4)));
    });
}

fn bench_formatting(c: &mut Criterion) {
    let mut group = c.benchmark_group("formatting");
    let date = NepaliDate::new(2077, 5, 19).unwrap();

    group.bench_function("format_simple", |b| {
        b.iter(|| black_box(date.format("%Y-%m-%d")));
    });

    group.bench_function("format_complex", |b| {
        b.iter(|| black_box(date.format_date("%d %B %Y")));
    });

    group.finish();
}

fn bench_date_arithmetic(c: &mut Criterion) {
    let date = NepaliDate::new(2077, 5, 19).unwrap();

    c.bench_function("add_days_small", |b| {
        b.iter(|| black_box(date.add_days(10)));
    });

    c.bench_function("add_days_large", |b| {
        b.iter(|| black_box(date.add_days(365)));
    });
}

criterion_group!(
    benches,
    bench_days_in_month,
    bench_date_creation,
    bench_bs_to_ad_conversion,
    bench_ad_to_bs_conversion,
    bench_formatting,
    bench_date_arithmetic
);
criterion_main!(benches);
