# System B accuracy comparison

**97/97 paired questions scored** with Groq GPT-OSS-120B at temperature zero. The question order was fixed by hashing IDs before the run. The team score uses numerical matching for numeric questions and key-point recall for qualitative and mixed questions. Both arms receive the same question and generation settings. Reference answers, expected figures and key points are used only in scoring.

| Measure | Original A | Revised B |
|---|---:|---:|
| Mean primary accuracy | 59.5% | 76.1% |
| Mean reported tokens per answer | 2313 | 2599 |

B scored higher on 22 questions, tied on 71 and scored lower on 4. The observed difference is 16.6 percentage points. This is a matched replay of a previously inspected benchmark.

## Method

A uses its original prompt and stored dense passages. B keeps its five stored cross-encoder selections and fills remaining slots from the stored dense list, up to ten distinct passages. Its prompt requests supported partial answers and calculations with units and cited inputs. This replay uses the archived A dense list as a proxy for B’s live dense ordering. One independent live adapter smoke test verified retrieval of ten distinct passages. The comparison tests the combination of retrieval and prompt changes.

Across all 97 questions, the offline evidence test found all required evidence for 55 with A, 60 with original B and 70 with the candidate. The original shared GPT-5.4 run remains separate from this Groq experiment. See [paired scores](paired_summary.json) for the included question IDs.
