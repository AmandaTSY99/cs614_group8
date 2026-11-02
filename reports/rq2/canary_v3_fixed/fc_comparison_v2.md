| System | Question | Type | Abstained | Current F1 | Recall / answer | Recall / answer+kp | Recall / question+answer+kp, high atomicity | Expected |
|---|---|---|---|---|---|---|---|---|
| A | gold-001 | numeric | no | 0.00 | 0.00 | 0.00 | 0.25 | 1.00 |
| B | gold-001 | numeric | no | 0.40 | 1.00 | 1.00 | 0.33 | 1.00 |
| C V1 | gold-001 | numeric | no | 0.40 | 0.67 | 1.00 | 0.33 | 1.00 |
| C V3 | gold-001 | numeric | no | 0.40 | 1.00 | 1.00 | 0.50 | 1.00 |
| A | gold-011 | numeric | yes | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| B | gold-011 | numeric | yes | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| C V1 | gold-011 | numeric | yes | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| C V3 | gold-011 | numeric | no | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 |
| A | gold-017 | qualitative | no | 0.40 | 0.50 | 0.25 | 0.40 | 0.67 |
| B | gold-017 | qualitative | no | 0.40 | 1.00 | 0.33 | 0.40 | 0.67 |
| C V1 | gold-017 | qualitative | no | 0.29 | 0.50 | 1.00 | 0.50 | 1.00 |
| C V3 | gold-017 | qualitative | no | 0.29 | 0.00 | 0.33 | 0.67 | 0.67 |
| A | gold-019 | qualitative | no | 0.88 | 1.00 | 1.00 | 1.00 | 1.00 |
| B | gold-019 | qualitative | no | 0.67 | 0.57 | 0.60 | 0.67 | 0.67 |
| C V1 | gold-019 | qualitative | no | 0.59 | 0.86 | 0.86 | 0.86 | 1.00 |
| C V3 | gold-019 | qualitative | no | 0.53 | 0.57 | 0.67 | 0.60 | 0.67 |
| A | gold-020 | qualitative | no | 0.50 | 0.50 | 0.43 | 0.67 | 1.00 |
| B | gold-020 | qualitative | no | 0.55 | 0.50 | 0.43 | 0.50 | 0.67 |
| C V1 | gold-020 | qualitative | no | 0.00 | 0.00 | 0.00 | 0.71 | 1.00 |
| C V3 | gold-020 | qualitative | no | 0.00 | 0.60 | 0.50 | 0.75 | 1.00 |

| Variant | Mean abs. difference from expected | Within 0.25 of expected |
|---|---|---|
| Current (F1, answer + key points) | 0.435 | 7 / 20 |
| Recall / answer | 0.320 | 11 / 20 |
| Recall / answer + key points | 0.280 | 12 / 20 |
| Recall / question + answer + key points, high atomicity | 0.294 | 10 / 20 |

| Check | Current F1 | Recall / answer | Recall / answer+kp | Recall / q+a+kp, high |
|---|---|---|---|---|
| gold-011, C v3 (correct calculation) >= 0.67 | FAIL (0.00) | FAIL (0.00) | FAIL (0.00) | FAIL (0.00) |
| gold-011 refusals (A, B, C v1) = 0 | PASS (0.00, 0.00, 0.00) | PASS (0.00, 0.00, 0.00) | PASS (0.00, 0.00, 0.00) | PASS (0.00, 0.00, 0.00) |
| gold-017, all systems >= 0.5 (rule: at least 3 of 4) | FAIL (0.40, 0.40, 0.29, 0.29) | FAIL (0.50, 1.00, 0.50, 0.00) | FAIL (0.25, 0.33, 1.00, 0.33) | FAIL (0.40, 0.40, 0.50, 0.67) |
| gold-020, C v1 and C v3 >= 0.5 | FAIL (0.00, 0.00) | FAIL (0.00, 0.60) | FAIL (0.00, 0.50) | PASS (0.71, 0.75) |

**ADOPT rule**

- Mean absolute difference <= 0.20: 0.294 -> FAIL
- gold-011 C v3 >= 0.67: 0.00 -> FAIL
- gold-020 C v1 and C v3 >= 0.5: 0.71, 0.75 -> PASS
- gold-017 >= 0.5 for at least 3 of 4 systems: 2 of 4 -> FAIL
- Result: **FALLBACK**

Judge cost for this re-scoring: $0.018
