---
tags:
  - Graph_Learning
  - Temporal_Networks
  - Congressional_Trading
  - AI_Governance
  - Mokslius_Protocol
date: 2026-02-08
author: Mokslius Protocol
source: https://arxiv.org/abs/2602.05514
paper_title: Detecting Information Channels in Congressional Trading via Temporal Graph Learning
authors: Benjamin Pham Roodman, Eugene Sy, J. Xavier Atero Vázquez, Yu-Shiang Huang, Che Lin, Chaun-Ju Wang
submitted: 2026-02-05
category: cs.CE
---

# Detecting Information Channels in Congressional Trading via Temporal Graph Learning

## Įvadas

**ArXiv ID:** 2602.05514
**Pateikimas:** 2026-02-05
**Kategorija:** Computer Science > Computational Engineering, Finance, and Science

**Autoriai:**
- Benjamin Pham Roodman
- Eugene Sy
- J. Xavier Atero Vázquez
- Yu-Shiang Huang
- Che Lin
- Chaun-Ju Wang

## 1. Problemos Formulavimas

### 1.1 Kontekstas

Kongreso narių prekyba akcijomis JAV kelia **informacijos asimetrijos** ir **interesų konfliktų** klausimus. Įstatymų leidėjai turi prieigą prie privilegijuotos informacijos, kuri gali turėti įtakos rinkų judėjimui.

**Esamos priežiūros problemos:**
- Tradiciniai metodai remiasi manual review arba simple heuristics
- Sunku identifikuoti complex temporal patterns
- Multi-modal ryšiai (lobbying, campaign finance, geographic ties) neintegruoti

### 1.2 Tyrimo Klausimas

Ar galima automatic detection congressional trades, kurios rodo statistically significant outperformance relative to market benchmarks, naudojant temporal graph networks?

## 2. Metodologija: Temporal Graph Network Framework

### 2.1 Duomenų Struktūra

**Dynamic Multi-Modal Graph:**

```
G = (V, E, T)

where:
V = Vertices (Lawmakers ∪ Corporations)
E = Edges (Trading, Lobbying, Campaign Finance, Geographic)
T = Temporal dimension (transaction timestamps)
```

**Node Types:**
1. **Congressional members** - Įstatymų leidėjai (Senate + House)
2. **Corporations** - Publicly traded companies

**Edge Types:**
1. **Trading edges** - Stock transactions (buy/sell)
2. **Lobbying edges** - Lobbying relationships
3. **Campaign finance edges** - Donations from corporate PACs
4. **Geographic edges** - District/state connections

### 2.2 Temporal Graph Network (TGN) Architecture

**Core Approach:** Dynamic edge classification

**TGN Components:**

1. **Message Function:**
   ```
   m_i(t) = MSG(s_i(t^-), s_j(t^-), Δt, e_{ij}(t))
   ```
   Aggregates information from source node `i`, destination node `j`, time delta, and edge features.

2. **Memory Update:**
   ```
   s_i(t) = MEM(s_i(t^-), m_i(t))
   ```
   Updates node state based on incoming messages.

3. **Embedding Function:**
   ```
   z_i(t) = EMB(s_i(t), τ)
   ```
   Generates node embeddings at query time `τ`.

### 2.3 Walk-Forward Validation Architecture

**Two-Step Design (prevencija look-ahead bias):**

**Step 1: Training Window**
- Historical data: [t₀, t₁]
- TGN learns temporal patterns

**Step 2: Validation Window**
- Future data: [t₁, t₂]
- Edge classification on unseen trades
- No future information leakage

**Temporal Split Example:**
```
Training: 2015-2020 → Validation: 2021-2022
```

### 2.4 Labeling Strategies

**Target Variable:** Trades exhibiting anomalous performance

**Risk-Adjusted Returns:**

1. **Sharpe Ratio:**
   ```
   S = (R_p - R_f) / σ_p

   where:
   R_p = Portfolio return
   R_f = Risk-free rate
   σ_p = Portfolio volatility
   ```

2. **Benchmark Comparison:**
   - Baseline: S&P 500 returns
   - Threshold: Statistical significance (e.g., p < 0.05)

**Label Assignment:**
```
Label = 1 if Trade outperforms S&P 500 (risk-adjusted)
Label = 0 otherwise
```

## 3. Duomenų Šaltiniai

### 3.1 Publicly Available Datasets

1. **STOCK Act Disclosures**
   - Congressional trading data
   - Required filings under Stop Trading on Congressional Knowledge Act (2012)
   - Fields: Transaction date, ticker, amount range, buy/sell

2. **Lobbying Disclosure Act Database**
   - Quarterly lobbying reports
   - Client-lobbyist-legislator relationships

3. **FEC Campaign Finance Data**
   - Federal Election Commission records
   - Corporate PAC contributions

4. **Geographic Data**
   - Congressional districts
   - Corporate headquarters locations

### 3.2 Data Integration Challenge

**Heterogeneous Sources → Unified Graph:**
- Entity resolution (matching lawmakers across datasets)
- Temporal alignment (synchronizing different reporting frequencies)
- Missing data handling

## 4. Eksperimentiniai Rezultatai

### 4.1 Hipotezė

TGN methods can **capture complex temporal dependencies** between:
- Congressional-corporate interactions (lobbying, donations)
- Subsequent trading outcomes (outperformance)

### 4.2 Validacijos Metrikos

**Classification Performance:**
- Precision: True positives / (True positives + False positives)
- Recall: True positives / (True positives + False negatives)
- F1-Score: Harmonic mean
- AUC-ROC: Area under curve

**Temporal Consistency:**
- Performance across multiple time horizons
- Stability of predictions over walk-forward windows

### 4.3 Findings (pagal abstraktą)

Paper demonstrates kad TGN framework **successfully captures temporal dependencies** tarp congressional-corporate interactions ir trading outcomes.

**Key Insight:** Multi-modal graph structure (trading + lobbying + finance + geography) suteikia richer signal nei isolated transaction analysis.

## 5. Technical Implementation Details

### 5.1 Graph Construction Pipeline

**Preprocessing Steps:**

1. **Entity Linking:**
   - Standardize lawmaker names across datasets
   - Match tickers to corporate entities
   - Resolve duplicates and variants

2. **Temporal Windowing:**
   - Define observation periods
   - Aggregate interactions within windows
   - Handle irregular time intervals

3. **Feature Engineering:**
   - Node features: Seniority, committee memberships, party affiliation
   - Edge features: Transaction amount, lobbying expenditure, donation size
   - Temporal features: Recency, frequency, duration

### 5.2 TGN Training

**Loss Function:**
```
L = Binary Cross-Entropy(y_pred, y_true)
```

**Optimization:**
- Adam optimizer
- Learning rate scheduling
- Early stopping on validation set

**Regularization:**
- Dropout on embeddings
- L2 weight decay

### 5.3 Computational Considerations

**Scalability:**
- 535 Congressional members (100 Senate + 435 House)
- Thousands of corporations
- Millions of edges (trades, lobbying acts, donations)
- Multi-year temporal span

**Efficiency Techniques:**
- Mini-batch temporal sampling
- Negative sampling for edge classification
- GPU acceleration for embedding updates

## 6. Interpretability ir Explainability

### 6.1 Attention Mechanisms

TGN can incorporate **attention weights** to identify:
- Which corporate relationships most predictive
- Which temporal patterns most salient
- Which graph neighborhoods most influential

### 6.2 Case Studies

Paper likely includes **concrete examples:**
- Specific trades flagged by model
- Temporal sequences leading to transactions
- Network paths connecting lawmakers to information sources

## 7. Ethical ir Regulatory Implications

### 7.1 Transparency

**Current Status:** STOCK Act requires disclosure, bet ne prevention

**AI Role:** Automated detection can:
- Surface suspicious patterns faster
- Reduce manual review burden
- Increase deterrent effect

### 7.2 False Positives

**Risk:** Flagging legitimate trades as suspicious

**Mitigation:**
- High precision thresholds
- Human-in-the-loop verification
- Statistical significance testing

### 7.3 Legal Considerations

**Inference ≠ Proof:**
- Model identifies **correlation**, ne causation
- Statistical patterns ne legal evidence
- Requires further investigation

## 8. Related Work

### 8.1 Congressional Trading Studies

**Prior Research:**
- Academic studies on congressional returns vs. market
- Findings vary: Some show outperformance, others null results
- Methodological debates on selection bias, survivorship bias

### 8.2 Graph Learning Applications

**Finance Domain:**
- Fraud detection in transaction networks
- Credit risk modeling with social graphs
- Market manipulation detection

**TGN Literature:**
- Dynamic link prediction
- Temporal knowledge graphs
- Continuous-time networks

## 9. Limitations

### 9.1 Data Quality

**Disclosure Delays:**
- STOCK Act allows 45-day reporting window
- Trades may be stale by analysis time

**Incomplete Information:**
- Some transactions in broad ranges ($1k-$15k, $15k-$50k)
- Spouse/dependent trades attributed to lawmaker
- Blind trusts excluded (may contain relevant activity)

### 9.2 Causality

**Correlation Challenges:**
- Outperformance may be coincidental
- Market movements driven by public information
- Difficult to isolate insider knowledge impact

### 9.3 Adversarial Considerations

**Gaming Risk:**
- Sophisticated actors may structure trades to evade detection
- Model opacity creates evasion opportunities
- Arms race between detection and avoidance

## 10. Future Directions

### 10.1 Expanded Data Integration

**Additional Signals:**
- Committee meeting attendance
- Legislative bill sponsorships
- Timing relative to corporate announcements
- Media coverage and sentiment

### 10.2 Real-Time Monitoring

**Deployment Scenario:**
- Continuous TGN updates as new disclosures arrive
- Alert system for anomalous patterns
- Dashboard for oversight bodies

### 10.3 Counterfactual Analysis

**What-If Scenarios:**
- Simulate impact of stricter trading rules
- Model behavior under alternative disclosure regimes
- Estimate deterrent effect of detection systems

## 11. Išvados

### 11.1 Technical Contribution

Paper demonstrates **Temporal Graph Networks** as viable approach for:
- Multi-modal data integration
- Dynamic pattern detection
- Long-horizon performance prediction

**Key Innovation:** Walk-forward validation architecture ensuring no look-ahead bias.

### 11.2 Practical Impact

**Oversight Enhancement:** AI-assisted detection can:
- Increase transparency
- Reduce investigation costs
- Strengthen accountability mechanisms

### 11.3 Broader Implications

**AI for Governance:** This work exemplifies using ML to:
- Monitor institutional behavior
- Detect conflicts of interest
- Support regulatory enforcement

**Replication Potential:** Methodology applicable to:
- Other legislative bodies
- Corporate insider trading
- Conflict of interest detection across sectors

---

## Technical Summary

**Problem:** Detect congressional trades exhibiting statistically significant outperformance

**Approach:** Temporal Graph Network integrating trading, lobbying, finance, geographic data

**Innovation:** Walk-forward validation preventing look-ahead bias

**Result:** TGN successfully captures complex temporal dependencies

**Significance:** Demonstrates AI viability for governance oversight and conflict detection

---

**Mokslius Protocol Pastaba:**

Šis paper reprezentuoja **AI-for-oversight** paradigmą - naudoti mašininio mokymosi metodus institucijų skaidrumo didinimui. Temporal graph approach elegantiškai sprendžia multi-modal data integration problemą ir temporal dependency modeling.

**Kritinė refleksija:** Nors technical contribution stiprus, practical deployment reikalauja clear ethical guidelines, legal framework coordination, ir safeguards prieš false positives bei adversarial gaming.

**Academic Rigor:** Methodology solidus, walk-forward validation tinkamas, bet paper turėtų include detailed ablation studies (koks contribution kiekvieno edge type), sensitivity analysis (threshold choices), ir comparative baselines (tradiciniai metodai).

Šis darbas bus citaras tiek AI/ML community (TGN applications), tiek public policy research (congressional oversight).
