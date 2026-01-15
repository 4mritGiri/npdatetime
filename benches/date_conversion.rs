use criterion::{black_box, criterion_group, criterion_main, Criterion};
use npdatetime::prelude::*;

fn bench_lookup(c: &mut Criterion) {
    let mut group = c.benchmark_group("Date Operations");
    
    group.bench_function("lookup::days_in_month", |b| {
        b.iter(|| {
            NepaliDate::days_in_month(black_box(2081), black_box(1)).unwrap()
        })
    });

    group.bench_function("lookup::to_gregorian", |b| {
        let date = NepaliDate::new(2081, 1, 1).unwrap();
        b.iter(|| {
            date.to_gregorian().unwrap()
        })
    });
    
    group.finish();
}

#[cfg(feature = "astronomical")]
fn bench_astronomical(c: &mut Criterion) {
    let mut group = c.benchmark_group("Date Operations");
    let cal = AstronomicalCalendar::new();

    group.bench_function("astronomical::calculate_month_days", |b| {
        b.iter(|| {
            cal.calculate_month_days(black_box(2081), black_box(1))
        })
    });

    group.bench_function("astronomical::get_year_info", |b| {
        b.iter(|| {
            cal.get_year_info(black_box(2081)).unwrap()
        })
    });

    group.finish();
}

#[cfg(not(feature = "astronomical"))]
criterion_group!(benches, bench_lookup);

#[cfg(feature = "astronomical")]
criterion_group!(benches, bench_lookup, bench_astronomical);

criterion_main!(benches);
