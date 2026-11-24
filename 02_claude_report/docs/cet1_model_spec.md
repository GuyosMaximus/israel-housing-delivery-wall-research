# CET1 erosion model: specification (Agent 3, 2026-11-24, written BEFORE the first run)

Nothing here may be changed after results are seen, except to fix a coding error (logged at the end).
Illustrative scenario. Not a Bank of Israel (BoI) or bank stress test.

## 1. Question and decision rule (fixed in advance)
REQ-H3-01, condition 2: bank loss < 10% of system equity. Numerator: system loss before tax, net of existing
provisions. Denominator: sum of shareholders' equity of the five groups, 30.9.2026.
Severe cell = the REQ's own worst corner: price fall q = 20%, delay m = 24 months, with buyer default d = 25%.
Rule: condition 2 is **met** if loss/equity < 10% under BOTH LGD variants (A and B, sec. 3) at the severe cell;
**not met** if >= 10% under both; **inconclusive / method-dependent** if they disagree.
Also reported, not part of the rule: the 5x5 grid, baseline, beyond-severe, per-bank CET1 vs its minimum, break-even.

## 2. Transmission: buyer default is NOT bank default
Chain: deferred-payment buyer fails at delivery (d) -> unit returns to the developer and is resold at (1-q)(1-c)
-> project cushion shrinks -> bank loses only where the cushion is exhausted.
Cushion = absorption capacity A ("maximum fall in apartment sale prices before the bank loses on the project", BoI).
Price-equivalent erosion of the unsold inventory:

    x(d,q,m) = q + [ p*phi*d*(1-(1-q)(1-c)) + O(m) ] / (1-p)

O(m) = delay cost per unit of project revenue, exactly the function of fig5.
Failed share of exposure PF = zeta * F(x). F = published cumulative distribution of A, by credit:
(0,0) (0.25,0.010) (0.30,0.08) (0.40,0.33) (0.50,0.556) (0.75,0.752) (1,1), linear between, 1 above 1.
Nodes 0.30, 0.40: BoI survey 2025 p.154 (end-2025, five groups, balance-sheet credit).
Nodes 0.25, 0.50, 0.75: Leumi Q3-2026 p.80 + Hapoalim Q3-2026 p.61, started projects, summed
(968; 54,630; 19,593; 24,771 of 99,962 NIS m). Two dates/populations are spliced: an approximation.

## 3. Loss
    EAD_b = s*D_b + delta*G_b
    A (conservative): L = EAD * PF * LGD,  LGD = 1-(1-q)(1-k)     (a failed project has zero cushion left)
    B (structural):   L = zeta * EAD * ((1-p)/(lambda+g)) * Integral_0^x F(a) da   (loss = depth of the shortfall only)
    Net loss  N_b = max(0, L_b - s*P_b);  dCET1 = N_b*(1-t)/RWA_b;  RWA static.
Variant A is the directive's EAD x failure x LGD form. The price fall enters both PF and LGD, so A overstates loss.
Variant B is the expected shortfall implied by the same distribution; it ignores fire-sale/legal costs, so it may understate.
No double counting: the guarantee is not an extra loss line. A drawn guarantee turns buyers' money into a bank claim on the
returned unit, so it is added to EAD and gets the same LGD. lambda = 0.7*0.83 = 0.581 (credit/revenue), g = 0.6*0.3 = 0.18.

## 4. Bank inputs (30.9.2026, NIS m): all read in the Q3-2026 reports
D = debts, construction + real-estate activity, Israel; T = total credit risk (on+off), same sectors; P = allowance, same;
G = outstanding guarantees to home buyers (nominal, gross of reinsurance); E = shareholders' equity.

| Bank | CET1 cap | RWA | CET1 % | Min % | D | T | P | G | E |
|---|---|---|---|---|---|---|---|---|---|
| Leumi | 70,936 | 623,358 | 11.38 | 10.23 | 149,317 | 238,418 | 3,368 | 47,972 | 71,442 |
| Hapoalim | 67,480 | 580,553 | 11.62 | 10.24 | 116,083 | 188,829 | 2,575 | 31,513 | 67,530 |
| Mizrahi-Tefahot | 37,170 | 368,119 | 10.10 | 9.60 | 54,442 | 98,698 | 709 | 18,293 | 36,667 |
| Discount | 35,821 | 347,080 | 10.32 | 9.21 | 56,484 | 90,415 | 1,251 | 17,480 | 35,098 |
| First Int'l | 14,730 | 143,282 | 10.28 | 9.24 | 24,491 | 36,206 | 469 | 2,984 | 14,533 |

Caveat: Hapoalim's E is total equity on the balance sheet. Tax 34.75% (2026, without the special tax): Discount/Leumi Q3-2026.
Stress floor 6.5%: BoI survey 2024, Box 5.1 (supervisory stress-test minimum).

## 5. Assumptions (calibrated)
| Par | Base | Rationale | Sensitivity |
|---|---|---|---|
| s | 150/367 = 0.409 | BoI survey 2025, table 5.1: residential projects 69 + residential land 81 of 367 bn; same share for all banks (no uniform bank split) | 69/367; 1.0 |
| delta | 1.0 | every guarantee of a failed project drawn, gross of reinsurance (conservative) | 0; 0.5 |
| d | grid 15-25% | fig4: share above the 50% PTI cap is 16.0% (base) and 26.7% (stress) | 0, 40% |
| q | grid 15-25% | Red Team directive; REQ goes to 20%; BoI scenario had 15% cumulative gap / fall | 5, 40% |
| m (grid) | 12 months | middle of the REQ range | 0, 24 |
| p, phi, c, O(m) | fig5 values (0.60, 0.45, 0.05) | one project model in the whole report | - |
| k | 5% | enforcement and selling cost, same size as the resale discount c | 10% |
| zeta | 1.0 | no refinancing / recourse mitigation (conservative) | 0.25, 0.5 |
| tax | 34.75% relief | statutory | 0% (shown as pre-tax) |
| A-definition | inventory base (divide by 1-p) | Leumi: "apartment inventory prices"; Hapoalim defines on completed value | divide by 1 |
Points: baseline (d 5%, q 5%, m 0); grid m=12; severe (25%,20%,24); beyond-severe (40%,40%,24).
Not modelled: pre-provision profit (cushion), second-round effects, other sectors' losses, mortgage-book losses, RWA
inflation, undrawn facilities (bounded by the T run: EAD = T, s = 1), land loans use the project distribution F.

## 6. Break-even (assumption-light)
(a) Loss rate on EAD at which each bank hits its minimum / the system hits 10% of equity:
    r* = (headroom*RWA/(1-t) + sP)/EAD.  (b) Price fall q* (d=25%, m=12 and 24) with the same condition, A and B.
Reference only: BoI 2025 survey stress test: system CET1 -1.5 pp (11.5 -> 10.0), cumulative C&RE loss 3.3% of that credit;
20.9% of NIS 84 bn = 17.6 bn. A full macro test with income and dynamic balance sheet, so not like-for-like.

## 7. Change log after first run
No parameter, equation or rule changed after the first run (2026-11-24). Only figure layout changed.
First-run verdict by the rule of sec. 1: condition 2 NOT MET at the severe cell (A 21.3%, B 14.2% of equity).

## 8. Hand check (Leumi, severe cell, variant A; arithmetic only, no import of the model)
O(24) = 0.45*0.1025 + 0.581*0.0725*2 + 0.27*0.5*0.055*2 + 0.6*7500*1.5*22/2.4m = 0.046125+0.084245+0.014850+0.061875 = 0.207095
buyers = 0.27*0.25*(1-0.8*0.95) = 0.0162;  x = 0.20 + 0.223295/0.4 = 0.758238
F = 0.752 + (0.008238/0.25)*0.248 = 0.760172;  LGD = 1-0.8*0.95 = 0.24;  rate = 0.182441
EAD = 0.408719*149,317 + 47,972 = 109,001;  gross = 19,886;  less 0.408719*3,368 = 1,377 -> 18,510
post-tax = 18,510*0.6525 = 12,077;  /623,358 = 193.7 bp;  CET1 = 11.38-1.94 = 9.44%  -> model 193.7 bp, 9.44%.
