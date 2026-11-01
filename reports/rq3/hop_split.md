# RQ3: accuracy on answers containing a number, by hop

Funnel: 97 benchmark questions -> 87 whose gold answer contains a number (73 multi-hop, 14 single-hop). Of these, 63 are labelled numeric or mixed in the benchmark.

| System | All | Single-hop | Multi-hop | Single -> multi | Typed numeric/mixed (all / single / multi) | Mean hops (single / multi) | p50 latency s (single / multi) |
|---|---|---|---|---|---|---|---|
| A | 71.3% (62/87) | 78.6% (11/14) | 69.9% (51/73) | -8.7 pp | 69.8% / 81.8% / 67.3% | 1.0 / 1.0 | 2.2 / 2.6 |
| B | 77.0% (67/87) | 85.7% (12/14) | 75.3% (55/73) | -10.4 pp | 71.4% / 81.8% / 69.2% | 1.0 / 1.0 | 7.3 / 8.0 |
| C v1 | 89.7% (78/87) | 100.0% (14/14) | 87.7% (64/73) | -12.3 pp | 85.7% / 100.0% / 82.7% | 1.64 / 2.33 | 9.4 / 22.0 |
| C v2 | 82.8% (72/87) | 92.9% (13/14) | 80.8% (59/73) | -12.1 pp | 76.2% / 90.9% / 73.1% | 1.43 / 1.77 | 8.9 / 14.9 |
| C v3 | 100.0% (87/87) | 100.0% (14/14) | 100.0% (73/73) | +0.0 pp | 100.0% / 100.0% / 100.0% | 1.79 / 2.18 | 7.8 / 18.4 |
