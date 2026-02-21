# Mariukas - Kling Batch Order v1

## Render strategy
1. Start with high-priority continuity anchors.
2. Run seed scan with 4 variants per shot.
3. Keep top 2 for continuity fix.
4. Final render only top 1.

## Priority order (top 20)
- S18 | Chorus A | 01:21-01:25 | score=130
- S10 | Chorus A | 00:46-00:50 | score=120
- S27 | Chorus B | 01:58-02:03 | score=115
- S13 | Chorus A | 00:59-01:03 | score=110
- S14 | Chorus A | 01:03-01:08 | score=110
- S26 | Chorus B | 01:54-01:58 | score=105
- S11 | Chorus A | 00:50-00:54 | score=100
- S12 | Chorus A | 00:54-00:59 | score=100
- S15 | Chorus A | 01:08-01:12 | score=100
- S16 | Chorus A | 01:12-01:16 | score=100
- S17 | Chorus A | 01:16-01:21 | score=100
- S05 | Verse 1 | 00:23-00:28 | score=95
- S09 | Verse 1 | 00:41-00:46 | score=95
- S28 | Chorus B | 02:03-02:07 | score=95
- S29 | Chorus B | 02:07-02:11 | score=95
- S30 | Chorus B | 02:11-02:15 | score=95
- S31 | Chorus B | 02:15-02:19 | score=95
- S32 | Chorus B | 02:19-02:24 | score=95
- S33 | Chorus B | 02:24-02:28 | score=95
- S34 | Chorus B | 02:28-02:32 | score=95

## Parallel batches
### Batch_1 (10 shots)
- S18, S26, S17, S30, S45, S04, S20, S25, S36, S41

### Batch_2 (10 shots)
- S10, S11, S05, S31, S48, S06, S21, S46, S37, S42

### Batch_3 (10 shots)
- S27, S12, S09, S32, S01, S07, S22, S47, S38, S44

### Batch_4 (9 shots)
- S13, S15, S28, S33, S02, S08, S23, S43, S39

### Batch_5 (9 shots)
- S14, S16, S29, S34, S03, S19, S24, S35, S40
