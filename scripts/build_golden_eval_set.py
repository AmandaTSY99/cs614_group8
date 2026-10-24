#!/usr/bin/env python3
"""
Canonical 50-Question Golden Evaluation Benchmark Builder for SEC 10-K Financial RAG.

Course: CS614 GenAI
Team Members:
- System A (Baseline): Naive single-pass dense retrieval (Amanda)
- System B (Advanced): Hybrid BM25 + BGE-m3 + Cross-Encoder reranker (Xavier & Kevin)
- System C (Proposed): Adaptive Multi-Hop LangGraph State Machine (Anish & Aryan)

Stratification:
- Tier 1: Single-Hop Factual (15 Questions — 1-2 per company)
- Tier 2: Quantitative Tabular + Narrative (20 Questions — 2 per company)
- Tier 3: Cross-Sectional Causal Chaining (15 Questions — 1-2 per company)
Total: 50 Questions (Exactly 5 per company across 10 companies)
"""

import json
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = REPO_ROOT / "data" / "golden_eval_set.json"

GOLDEN_QUESTIONS: List[Dict[str, Any]] = [
    # =========================================================================
    # TIER 1: Single-Hop Factual (15 Questions — 1-2 per company)
    # Target: Factual disclosures, period end dates, independent auditors,
    # state of incorporation, corporate address, discrete risk definitions.
    # Purpose: Tests whether System C's Evidence Sufficiency Critic correctly
    # early-stops at Hop 1 without wasting tokens/latency.
    # Category label: "single_hop_factual"
    # =========================================================================
    {
        "id": "GOLD-01",
        "ticker": "NVDA",
        "fiscal_years": [2026],
        "category": "single_hop_factual",
        "min_required_hops": 1,
        "query": "What was NVIDIA's fiscal year 2026 period end date, and where is its principal executive office located?",
        "target_sections": ["Item 1", "Item 8"],
        "ground_truth_answer": "NVIDIA's fiscal year 2026 ended on January 25, 2026, and its principal executive office is located at 2788 San Tomas Expressway, Santa Clara, California 95051.",
        "ground_truth_numbers": ["January 25, 2026", "95051"],
    },
    {
        "id": "GOLD-02",
        "ticker": "AAPL",
        "fiscal_years": [2024],
        "category": "single_hop_factual",
        "min_required_hops": 1,
        "query": "Who served as Apple Inc.'s independent registered public accounting firm for the fiscal year ended September 28, 2024?",
        "target_sections": ["Item 8", "Item 14"],
        "ground_truth_answer": "Ernst & Young LLP served as Apple Inc.'s independent registered public accounting firm for the fiscal year ended September 28, 2024.",
        "ground_truth_numbers": ["September 28, 2024"],
    },
    {
        "id": "GOLD-03",
        "ticker": "AAPL",
        "fiscal_years": [2024],
        "category": "single_hop_factual",
        "min_required_hops": 1,
        "query": "What is Apple Inc.'s state of incorporation, corporate headquarters address, and IRS employer identification number in its 2024 Form 10-K?",
        "target_sections": ["Item 1"],
        "ground_truth_answer": "Apple Inc. is incorporated in the State of California, with principal executive offices at One Apple Park Way, Cupertino, California 95014, and IRS Employer Identification No. 94-2404110.",
        "ground_truth_numbers": ["95014", "94-2404110"],
    },
    {
        "id": "GOLD-04",
        "ticker": "MSFT",
        "fiscal_years": [2024],
        "category": "single_hop_factual",
        "min_required_hops": 1,
        "query": "Under the laws of which state is Microsoft Corporation incorporated, and what is the address of its corporate headquarters?",
        "target_sections": ["Item 1"],
        "ground_truth_answer": "Microsoft Corporation is incorporated under the laws of the State of Washington, with corporate headquarters at One Microsoft Way, Redmond, Washington 98052-6399.",
        "ground_truth_numbers": ["98052-6399"],
    },
    {
        "id": "GOLD-05",
        "ticker": "MSFT",
        "fiscal_years": [2024],
        "category": "single_hop_factual",
        "min_required_hops": 1,
        "query": "Who served as Microsoft Corporation's independent auditor for the fiscal year ended June 30, 2024, and what is its IRS employer identification number?",
        "target_sections": ["Item 1", "Item 8", "Item 14"],
        "ground_truth_answer": "Deloitte & Touche LLP served as Microsoft Corporation's independent auditor for the fiscal year ended June 30, 2024, and Microsoft's IRS employer identification number is 91-1144442.",
        "ground_truth_numbers": ["June 30, 2024", "91-1144442"],
    },
    {
        "id": "GOLD-06",
        "ticker": "AMZN",
        "fiscal_years": [2024],
        "category": "single_hop_factual",
        "min_required_hops": 1,
        "query": "What is Amazon.com, Inc.'s state of incorporation, corporate headquarters address, and IRS employer identification number as disclosed in its 2024 Form 10-K?",
        "target_sections": ["Item 1"],
        "ground_truth_answer": "Amazon.com, Inc. is incorporated in Delaware, with principal executive offices located at 410 Terry Avenue North, Seattle, Washington 98109-5210, and IRS Employer Identification No. 91-1646860.",
        "ground_truth_numbers": ["98109-5210", "91-1646860"],
    },
    {
        "id": "GOLD-07",
        "ticker": "AMZN",
        "fiscal_years": [2024],
        "category": "single_hop_factual",
        "min_required_hops": 1,
        "query": "Who served as Amazon.com, Inc.'s independent registered public accounting firm for the fiscal year ended December 31, 2024?",
        "target_sections": ["Item 8", "Item 14"],
        "ground_truth_answer": "Ernst & Young LLP served as Amazon.com, Inc.'s independent registered public accounting firm for the fiscal year ended December 31, 2024.",
        "ground_truth_numbers": ["December 31, 2024"],
    },
    {
        "id": "GOLD-08",
        "ticker": "GOOGL",
        "fiscal_years": [2024],
        "category": "single_hop_factual",
        "min_required_hops": 1,
        "query": "What is Alphabet Inc.'s principal executive offices address, state of incorporation, and Commission file number in its 2024 Form 10-K?",
        "target_sections": ["Item 1"],
        "ground_truth_answer": "Alphabet Inc. is incorporated in Delaware, with principal executive offices at 1600 Amphitheatre Parkway, Mountain View, California 94043, and Commission file number 001-37580.",
        "ground_truth_numbers": ["94043", "001-37580"],
    },
    {
        "id": "GOLD-09",
        "ticker": "GOOGL",
        "fiscal_years": [2024],
        "category": "single_hop_factual",
        "min_required_hops": 1,
        "query": "Who served as Alphabet Inc.'s independent auditor for the fiscal year ended December 31, 2024, and what was its IRS employer identification number?",
        "target_sections": ["Item 1", "Item 8", "Item 14"],
        "ground_truth_answer": "Ernst & Young LLP served as Alphabet Inc.'s independent registered public accounting firm for the fiscal year ended December 31, 2024, and its IRS employer identification number is 61-1767919.",
        "ground_truth_numbers": ["December 31, 2024", "61-1767919"],
    },
    {
        "id": "GOLD-10",
        "ticker": "META",
        "fiscal_years": [2024],
        "category": "single_hop_factual",
        "min_required_hops": 1,
        "query": "What is Meta Platforms, Inc.'s state of incorporation, corporate headquarters address, and IRS employer identification number in its 2024 Form 10-K?",
        "target_sections": ["Item 1"],
        "ground_truth_answer": "Meta Platforms, Inc. is incorporated in Delaware, with principal executive offices at 1 Meta Way, Menlo Park, California 94025, and IRS Employer Identification No. 20-1665019.",
        "ground_truth_numbers": ["94025", "20-1665019"],
    },
    {
        "id": "GOLD-11",
        "ticker": "META",
        "fiscal_years": [2024],
        "category": "single_hop_factual",
        "min_required_hops": 1,
        "query": "Who served as the independent registered public accounting firm for Meta Platforms, Inc. for the fiscal year ended December 31, 2024?",
        "target_sections": ["Item 8", "Item 14"],
        "ground_truth_answer": "Ernst & Young LLP served as Meta Platforms, Inc.'s independent registered public accounting firm for the fiscal year ended December 31, 2024.",
        "ground_truth_numbers": ["December 31, 2024"],
    },
    {
        "id": "GOLD-12",
        "ticker": "TSLA",
        "fiscal_years": [2024],
        "category": "single_hop_factual",
        "min_required_hops": 1,
        "query": "What state of incorporation, principal executive office address, and independent registered public accounting firm are disclosed in Tesla, Inc.'s 2024 Form 10-K?",
        "target_sections": ["Item 1", "Item 8"],
        "ground_truth_answer": "Tesla, Inc. is incorporated in Texas, located at 1 Tesla Road, Austin, Texas 78725, with PricewaterhouseCoopers LLP serving as its independent registered public accounting firm for the fiscal year ended December 31, 2024.",
        "ground_truth_numbers": ["78725", "December 31, 2024"],
    },
    {
        "id": "GOLD-13",
        "ticker": "JPM",
        "fiscal_years": [2024],
        "category": "single_hop_factual",
        "min_required_hops": 1,
        "query": "Where are JPMorgan Chase & Co.'s principal executive offices located, and under what state laws is the firm incorporated?",
        "target_sections": ["Item 1"],
        "ground_truth_answer": "JPMorgan Chase & Co. is incorporated under the laws of the State of Delaware, with principal executive offices located at 270 Park Avenue, New York, New York 10017.",
        "ground_truth_numbers": ["10017"],
    },
    {
        "id": "GOLD-14",
        "ticker": "JNJ",
        "fiscal_years": [2024],
        "category": "single_hop_factual",
        "min_required_hops": 1,
        "query": "What was Johnson & Johnson's fiscal year 2024 period end date, where is its principal corporate office located, and under which state is it incorporated?",
        "target_sections": ["Item 1", "Item 8"],
        "ground_truth_answer": "Johnson & Johnson's fiscal year 2024 ended on December 29, 2024, its principal corporate office is located at One Johnson & Johnson Plaza, New Brunswick, New Jersey 08933, and it is incorporated in New Jersey.",
        "ground_truth_numbers": ["December 29, 2024", "08933"],
    },
    {
        "id": "GOLD-15",
        "ticker": "WMT",
        "fiscal_years": [2025],
        "category": "single_hop_factual",
        "min_required_hops": 1,
        "query": "What is Walmart Inc.'s principal executive office address, state of incorporation, and independent registered public accounting firm for the fiscal year ended January 31, 2025?",
        "target_sections": ["Item 1", "Item 8"],
        "ground_truth_answer": "Walmart Inc. is incorporated in Delaware, with principal executive offices located at 1 Customer Drive, Bentonville, AR 72716, and Ernst & Young LLP served as its independent registered public accounting firm for the fiscal year ended January 31, 2025.",
        "ground_truth_numbers": ["72716", "January 31, 2025"],
    },

    # =========================================================================
    # TIER 2: Quantitative Tabular + Narrative (20 Questions — 2 per company)
    # Target: TAT-QA style joint text + table reasoning (multi-year revenue/income,
    # segment margins, cash flows). Verified against data/financials.csv.
    # Evaluates tabular grounding and tests System C v2's autonomous tabular_tool.
    # Category label: "quantitative_tabular"
    # =========================================================================
    {
        "id": "GOLD-16",
        "ticker": "NVDA",
        "fiscal_years": [2025, 2026],
        "category": "quantitative_tabular",
        "min_required_hops": 2,
        "query": "Compare NVIDIA's total revenue, operating income, and net income between FY2025 and FY2026, and calculate the year-over-year revenue growth rate.",
        "target_sections": ["Item 8 Financial Statements", "financials.csv"],
        "ground_truth_answer": "In FY2025, NVIDIA reported Revenue of $130,497 million, Operating Income of $81,453 million, and Net Income of $72,880 million. In FY2026, Revenue increased to $215,938 million, Operating Income increased to $130,387 million, and Net Income rose to $120,067 million, representing a year-over-year revenue growth of 65.5%.",
        "ground_truth_numbers": ["$130,497 million", "$81,453 million", "$72,880 million", "$215,938 million", "$130,387 million", "$120,067 million", "65.5%"],
    },
    {
        "id": "GOLD-17",
        "ticker": "NVDA",
        "fiscal_years": [2025, 2026],
        "category": "quantitative_tabular",
        "min_required_hops": 2,
        "query": "What was NVIDIA's operating cash flow, total assets, and diluted earnings per share in FY2025 versus FY2026?",
        "target_sections": ["Item 8 Financial Statements", "financials.csv"],
        "ground_truth_answer": "In FY2025, NVIDIA recorded Operating Cash Flow of $64,089 million, Total Assets of $111,601 million, and Diluted EPS of $2.94. In FY2026, Operating Cash Flow rose to $102,718 million, Total Assets increased to $206,803 million, and Diluted EPS rose to $4.90.",
        "ground_truth_numbers": ["$64,089 million", "$111,601 million", "$2.94", "$102,718 million", "$206,803 million", "$4.90"],
    },
    {
        "id": "GOLD-18",
        "ticker": "AAPL",
        "fiscal_years": [2023, 2024],
        "category": "quantitative_tabular",
        "min_required_hops": 2,
        "query": "What was Apple's total net sales, gross margin, and operating cash flow in fiscal 2023 versus fiscal 2024?",
        "target_sections": ["Item 8 Financial Statements", "financials.csv"],
        "ground_truth_answer": "In fiscal 2023, Apple recorded total net sales of $383,285 million, gross margin of $169,148 million (44.1%), and cash flow from operations of $110,543 million. In fiscal 2024, net sales rose to $391,035 million, gross margin grew to $180,683 million (46.2%), and operating cash flow increased to $118,254 million.",
        "ground_truth_numbers": ["$383,285 million", "$391,035 million", "44.1%", "46.2%", "$110,543 million", "$118,254 million"],
    },
    {
        "id": "GOLD-19",
        "ticker": "AAPL",
        "fiscal_years": [2023, 2024],
        "category": "quantitative_tabular",
        "min_required_hops": 2,
        "query": "Compare Apple's operating income, net income, and diluted EPS between fiscal 2023 and fiscal 2024.",
        "target_sections": ["Item 8 Financial Statements", "financials.csv"],
        "ground_truth_answer": "In fiscal 2023, Apple reported operating income of $114,301 million, net income of $96,995 million, and diluted EPS of $6.13. In fiscal 2024, operating income increased to $123,216 million (up 7.8%), net income was $93,736 million, and diluted EPS was $6.08.",
        "ground_truth_numbers": ["$114,301 million", "$123,216 million", "$96,995 million", "$93,736 million", "$6.13", "$6.08", "7.8%"],
    },
    {
        "id": "GOLD-20",
        "ticker": "MSFT",
        "fiscal_years": [2023, 2024],
        "category": "quantitative_tabular",
        "min_required_hops": 2,
        "query": "Compare Microsoft's total revenue, net income, and diluted EPS between FY2023 and FY2024.",
        "target_sections": ["Item 8 Financial Statements", "financials.csv"],
        "ground_truth_answer": "In FY2023, Microsoft reported total revenue of $211,915 million, net income of $72,361 million, and diluted EPS of $9.68. In FY2024, total revenue increased to $245,122 million (up 16%), net income grew to $88,136 million (up 22%), and diluted EPS increased to $11.80.",
        "ground_truth_numbers": ["$211,915 million", "$245,122 million", "$72,361 million", "$88,136 million", "$9.68", "$11.80", "16%", "22%"],
    },
    {
        "id": "GOLD-21",
        "ticker": "MSFT",
        "fiscal_years": [2023, 2024],
        "category": "quantitative_tabular",
        "min_required_hops": 2,
        "query": "What were Microsoft's operating income, operating cash flow, and total assets in FY2023 versus FY2024?",
        "target_sections": ["Item 8 Financial Statements", "financials.csv"],
        "ground_truth_answer": "In FY2023, Microsoft recorded operating income of $88,523 million, cash flow from operations of $87,582 million, and total assets of $411,976 million. In FY2024, operating income rose to $109,433 million, operating cash flow reached $118,548 million, and total assets expanded to $512,163 million.",
        "ground_truth_numbers": ["$88,523 million", "$109,433 million", "$87,582 million", "$118,548 million", "$411,976 million", "$512,163 million"],
    },
    {
        "id": "GOLD-22",
        "ticker": "AMZN",
        "fiscal_years": [2023, 2024],
        "category": "quantitative_tabular",
        "min_required_hops": 2,
        "query": "Compare Amazon's net sales, operating income, and operating cash flow between 2023 and 2024.",
        "target_sections": ["Item 8 Financial Statements", "financials.csv"],
        "ground_truth_answer": "In 2023, Amazon reported net sales of $574,785 million, operating income of $36,852 million, and operating cash flow of $84,946 million. In 2024, net sales grew to $637,959 million (up 11%), operating income nearly doubled to $68,593 million (up 86%), and operating cash flow increased to $115,877 million.",
        "ground_truth_numbers": ["$574,785 million", "$637,959 million", "$36,852 million", "$68,593 million", "$84,946 million", "$115,877 million", "11%", "86%"],
    },
    {
        "id": "GOLD-23",
        "ticker": "AMZN",
        "fiscal_years": [2023, 2024],
        "category": "quantitative_tabular",
        "min_required_hops": 2,
        "query": "What was Amazon's net income, total assets, and diluted earnings per share in 2023 compared to 2024?",
        "target_sections": ["Item 8 Financial Statements", "financials.csv"],
        "ground_truth_answer": "In 2023, Amazon recorded net income of $30,425 million, total assets of $527,854 million, and diluted EPS of $2.90. In 2024, net income increased to $59,248 million (up 95%), total assets grew to $624,894 million, and diluted EPS rose to $5.53.",
        "ground_truth_numbers": ["$30,425 million", "$59,248 million", "$527,854 million", "$624,894 million", "$2.90", "$5.53", "95%"],
    },
    {
        "id": "GOLD-24",
        "ticker": "GOOGL",
        "fiscal_years": [2023, 2024],
        "category": "quantitative_tabular",
        "min_required_hops": 2,
        "query": "Compare Alphabet's revenues, operating income, and operating margin between 2023 and 2024.",
        "target_sections": ["Item 8 Financial Statements", "financials.csv"],
        "ground_truth_answer": "In 2023, Alphabet generated revenues of $307,394 million and operating income of $84,293 million, resulting in an operating margin of 27.4%. In 2024, revenues grew to $350,018 million (up 14%) and operating income rose to $112,390 million, expanding the operating margin to 32.1%.",
        "ground_truth_numbers": ["$307,394 million", "$350,018 million", "$84,293 million", "$112,390 million", "27.4%", "32.1%", "14%"],
    },
    {
        "id": "GOLD-25",
        "ticker": "GOOGL",
        "fiscal_years": [2023, 2024],
        "category": "quantitative_tabular",
        "min_required_hops": 2,
        "query": "What were Alphabet's net income, operating cash flow, and diluted earnings per share in 2023 versus 2024?",
        "target_sections": ["Item 8 Financial Statements", "financials.csv"],
        "ground_truth_answer": "In 2023, Alphabet reported net income of $73,795 million, cash flow from operations of $101,746 million, and diluted EPS of $5.80. In 2024, net income rose to $100,118 million (up 36%), operating cash flow grew to $125,299 million, and diluted EPS reached $8.04.",
        "ground_truth_numbers": ["$73,795 million", "$100,118 million", "$101,746 million", "$125,299 million", "$5.80", "$8.04", "36%"],
    },
    {
        "id": "GOLD-26",
        "ticker": "META",
        "fiscal_years": [2023, 2024],
        "category": "quantitative_tabular",
        "min_required_hops": 2,
        "query": "Compare Meta's total revenue, operating income, and net income between 2023 and 2024, and calculate the year-over-year revenue growth rate.",
        "target_sections": ["Item 8 Financial Statements", "financials.csv"],
        "ground_truth_answer": "In 2023, Meta generated total revenue of $134,902 million, operating income of $46,751 million, and net income of $39,098 million. In 2024, total revenue rose to $164,501 million, operating income surged to $69,380 million, and net income increased to $62,360 million, representing year-over-year revenue growth of 21.9%.",
        "ground_truth_numbers": ["$134,902 million", "$164,501 million", "$46,751 million", "$69,380 million", "$39,098 million", "$62,360 million", "21.9%"],
    },
    {
        "id": "GOLD-27",
        "ticker": "META",
        "fiscal_years": [2023, 2024],
        "category": "quantitative_tabular",
        "min_required_hops": 2,
        "query": "What were Meta's cash and cash equivalents, operating cash flow, and diluted EPS in 2023 versus 2024?",
        "target_sections": ["Item 8 Financial Statements", "financials.csv"],
        "ground_truth_answer": "In 2023, Meta held cash and cash equivalents of $41,862 million, generated operating cash flow of $71,113 million, and reported diluted EPS of $14.87. In 2024, cash and cash equivalents were $43,889 million, operating cash flow reached $91,328 million, and diluted EPS increased to $23.86.",
        "ground_truth_numbers": ["$41,862 million", "$43,889 million", "$71,113 million", "$91,328 million", "$14.87", "$23.86"],
    },
    {
        "id": "GOLD-28",
        "ticker": "TSLA",
        "fiscal_years": [2023, 2024],
        "category": "quantitative_tabular",
        "min_required_hops": 2,
        "query": "Compare Tesla's total revenues, net income, and diluted EPS between 2023 and 2024, and calculate the percentage change in net income.",
        "target_sections": ["Item 8 Financial Statements", "financials.csv"],
        "ground_truth_answer": "In 2023, Tesla reported total revenues of $96,773 million, net income of $14,997 million, and diluted EPS of $4.30. In 2024, total revenues were $97,690 million, net income dropped to $7,091 million (a 52.7% decrease), and diluted EPS decreased to $2.04.",
        "ground_truth_numbers": ["$96,773 million", "$97,690 million", "$14,997 million", "$7,091 million", "52.7%", "$4.30", "$2.04"],
    },
    {
        "id": "GOLD-29",
        "ticker": "TSLA",
        "fiscal_years": [2023, 2024],
        "category": "quantitative_tabular",
        "min_required_hops": 2,
        "query": "What were Tesla's operating income, operating cash flow, and total assets in 2023 versus 2024?",
        "target_sections": ["Item 8 Financial Statements", "financials.csv"],
        "ground_truth_answer": "In 2023, Tesla recorded operating income of $8,891 million, cash flow from operations of $13,256 million, and total assets of $106,618 million. In 2024, operating income was $7,076 million, operating cash flow increased to $14,923 million, and total assets grew to $122,070 million.",
        "ground_truth_numbers": ["$8,891 million", "$7,076 million", "$13,256 million", "$14,923 million", "$106,618 million", "$122,070 million"],
    },
    {
        "id": "GOLD-30",
        "ticker": "JPM",
        "fiscal_years": [2023, 2024],
        "category": "quantitative_tabular",
        "min_required_hops": 2,
        "query": "Compare JPMorgan Chase's total net revenue, net income, and diluted EPS between 2023 and 2024.",
        "target_sections": ["Item 8 Financial Statements", "financials.csv"],
        "ground_truth_answer": "In 2023, JPMorgan Chase reported total net revenue of $158,104 million, net income of $49,552 million, and diluted EPS of $16.23. In 2024, total net revenue increased to $177,556 million (up 12.3%), net income rose to $58,471 million (up 18.0%), and diluted EPS reached $19.75.",
        "ground_truth_numbers": ["$158,104 million", "$177,556 million", "$49,552 million", "$58,471 million", "$16.23", "$19.75", "12.3%", "18.0%"],
    },
    {
        "id": "GOLD-31",
        "ticker": "JPM",
        "fiscal_years": [2023, 2024],
        "category": "quantitative_tabular",
        "min_required_hops": 2,
        "query": "What were JPMorgan Chase's total assets, total liabilities, and stockholders' equity at year-end 2023 compared to 2024?",
        "target_sections": ["Item 8 Financial Statements", "financials.csv"],
        "ground_truth_answer": "As of December 31, 2023, JPMorgan Chase reported total assets of $3,875,393 million, total liabilities of $3,547,515 million, and stockholders' equity of $327,878 million. As of December 31, 2024, total assets grew to $4,002,814 million, total liabilities were $3,658,056 million, and stockholders' equity increased to $344,758 million.",
        "ground_truth_numbers": ["$3,875,393 million", "$4,002,814 million", "$3,547,515 million", "$3,658,056 million", "$327,878 million", "$344,758 million"],
    },
    {
        "id": "GOLD-32",
        "ticker": "JNJ",
        "fiscal_years": [2023, 2024],
        "category": "quantitative_tabular",
        "min_required_hops": 2,
        "query": "Compare Johnson & Johnson's total sales, net earnings, and diluted earnings per share from continuing operations between 2023 and 2024.",
        "target_sections": ["Item 8 Financial Statements", "financials.csv"],
        "ground_truth_answer": "In 2023, Johnson & Johnson reported total sales of $85,159 million, total net earnings of $35,153 million (inclusive of Kenvue discontinued operations gain), with continuing operations diluted EPS of $5.20 (and total diluted EPS of $13.72). In 2024, total sales rose to $88,821 million (up 4.3%), net earnings were $14,066 million, and diluted EPS was $5.79.",
        "ground_truth_numbers": ["$85,159 million", "$88,821 million", "$35,153 million", "$14,066 million", "$5.79", "4.3%"],
    },
    {
        "id": "GOLD-33",
        "ticker": "JNJ",
        "fiscal_years": [2023, 2024],
        "category": "quantitative_tabular",
        "min_required_hops": 2,
        "query": "What were Johnson & Johnson's operating cash flow, total assets, and total liabilities at the end of fiscal 2023 versus fiscal 2024?",
        "target_sections": ["Item 8 Financial Statements", "financials.csv"],
        "ground_truth_answer": "For fiscal 2023, Johnson & Johnson generated operating cash flow of $22,791 million, with total assets of $167,558 million and total liabilities of $98,784 million. For fiscal 2024, operating cash flow increased to $24,266 million, total assets expanded to $180,104 million, and total liabilities were $108,614 million.",
        "ground_truth_numbers": ["$22,791 million", "$24,266 million", "$167,558 million", "$180,104 million", "$98,784 million", "$108,614 million"],
    },
    {
        "id": "GOLD-34",
        "ticker": "WMT",
        "fiscal_years": [2024, 2025],
        "category": "quantitative_tabular",
        "min_required_hops": 2,
        "query": "Compare Walmart's total revenues, operating income, and consolidated net income between FY2024 and FY2025.",
        "target_sections": ["Item 8 Financial Statements", "financials.csv"],
        "ground_truth_answer": "In FY2024, Walmart reported total revenues of $648,125 million, operating income of $27,012 million, and consolidated net income of $15,511 million. In FY2025, total revenues grew to $680,985 million (up 5.1%), operating income increased to $29,348 million (up 8.6%), and consolidated net income rose to $19,436 million (up 25.3%).",
        "ground_truth_numbers": ["$648,125 million", "$680,985 million", "$27,012 million", "$29,348 million", "$15,511 million", "$19,436 million", "5.1%", "8.6%", "25.3%"],
    },
    {
        "id": "GOLD-35",
        "ticker": "WMT",
        "fiscal_years": [2024, 2025],
        "category": "quantitative_tabular",
        "min_required_hops": 2,
        "query": "What were Walmart's operating cash flow, total assets, and diluted earnings per share in FY2024 versus FY2025?",
        "target_sections": ["Item 8 Financial Statements", "financials.csv"],
        "ground_truth_answer": "In FY2024, Walmart recorded operating cash flow of $35,726 million, total assets of $252,399 million, and diluted EPS of $1.91. In FY2025, operating cash flow increased to $36,443 million, total assets expanded to $260,823 million, and diluted EPS grew to $2.41.",
        "ground_truth_numbers": ["$35,726 million", "$36,443 million", "$252,399 million", "$260,823 million", "$1.91", "$2.41"],
    },

    # =========================================================================
    # TIER 3: Cross-Sectional Causal Chaining (15 Questions — 1-2 per company)
    # Target: Multi-hop questions where clues are scattered across non-adjacent
    # sections (Item 7 MD&A to Item 8 Notes, Item 7A to Hedging, Item 3 to
    # Loss Contingencies). Core battleground for RQ1 and RQ2.
    # Category label: "cross_section_multihop"
    # =========================================================================
    {
        "id": "GOLD-36",
        "ticker": "NVDA",
        "fiscal_years": [2026],
        "category": "cross_section_multihop",
        "min_required_hops": 2,
        "query": "How did NVIDIA's Compute & Networking segment perform in FY2026, and what specific direct customer concentration percentages were disclosed in the Notes to Consolidated Financial Statements?",
        "target_sections": ["Item 7", "Item 8 Note on Concentration of Revenue"],
        "ground_truth_answer": "NVIDIA's Compute & Networking segment revenue increased 67% to $193,479 million in FY2026 (from $116,193 million in FY2025), with segment operating income rising 57% to $130,141 million, driven by the Blackwell and Hopper computing platforms and a 142% surge in Data Center networking. In the Concentration of Revenue note disclosures, NVIDIA reported that sales to one direct customer represented 22% of total revenue and sales to another direct customer represented 14% of total revenue in fiscal year 2026, with both concentrated primarily within Compute & Networking.",
        "ground_truth_numbers": ["$193,479 million", "67%", "$130,141 million", "22%", "14%"],
    },
    {
        "id": "GOLD-37",
        "ticker": "NVDA",
        "fiscal_years": [2026],
        "category": "cross_section_multihop",
        "min_required_hops": 2,
        "query": "What sensitivity to interest rate shifts and public equity price movements did NVIDIA disclose in Item 7A, and what senior notes balance was reported in Note 11?",
        "target_sections": ["Item 7A", "Item 8 Note 11"],
        "ground_truth_answer": "In Item 7A, NVIDIA disclosed that a 0.5% decrease in the yield curve would decrease the fair value of its fixed-rate investment portfolio by approximately $0.2 billion as of fiscal year-end 2026 and 2025, while a hypothetical 10% decrease in publicly-held equity securities would reduce their fair value by $1.8 billion. Furthermore, NVIDIA carried $8.5 billion of senior notes outstanding at fixed interest rates, as detailed in Note 11.",
        "ground_truth_numbers": ["0.5%", "$0.2 billion", "10%", "$1.8 billion", "$8.5 billion"],
    },
    {
        "id": "GOLD-38",
        "ticker": "AAPL",
        "fiscal_years": [2024],
        "category": "cross_section_multihop",
        "min_required_hops": 2,
        "query": "How did Apple's iPhone and Services product revenues perform in fiscal 2024 according to Item 7, and how did this compare to regional net sales in Americas and Greater China disclosed in Note 13?",
        "target_sections": ["Item 7", "Item 8 Note 13"],
        "ground_truth_answer": "In Item 7, Apple reported fiscal 2024 iPhone net sales of $201,183 million (flat compared to $200,583 million in 2023) and Services net sales growth of 12.9% to $96,169 million (up from $85,200 million). In Note 13 Segment Information, Americas net sales expanded to $167,045 million with operating income of $67,656 million, whereas Greater China net sales declined from $72,559 million in 2023 to $66,952 million in 2024 (with operating income falling to $27,082 million), primarily reflecting lower iPhone net sales and currency headwinds.",
        "ground_truth_numbers": ["$201,183 million", "$96,169 million", "$167,045 million", "$67,656 million", "$72,559 million", "$66,952 million", "$27,082 million"],
    },
    {
        "id": "GOLD-39",
        "ticker": "MSFT",
        "fiscal_years": [2024],
        "category": "cross_section_multihop",
        "min_required_hops": 2,
        "query": "What revenue and operating income did Microsoft report for Intelligent Cloud in FY2024 according to Note 19, and what drivers were cited in Item 7 MD&A alongside goodwill recorded for Activision Blizzard?",
        "target_sections": ["Item 7", "Item 8 Note 8", "Item 8 Note 19"],
        "ground_truth_answer": "In Note 19, Microsoft reported that Intelligent Cloud revenue grew 20% to $105,362 million in FY2024 (from $87,907 million in FY2023) and operating income grew 31% to $49,584 million. In Item 7 MD&A, management cited Azure and other cloud services revenue growth of 30% as the primary driver. Additionally, Note 8 and Note 19 disclosed $51.0 billion of goodwill recognized in connection with the acquisition of Activision Blizzard within the More Personal Computing segment.",
        "ground_truth_numbers": ["$105,362 million", "$49,584 million", "20%", "31%", "30%", "$51.0 billion"],
    },
    {
        "id": "GOLD-40",
        "ticker": "AMZN",
        "fiscal_years": [2024],
        "category": "cross_section_multihop",
        "min_required_hops": 2,
        "query": "How did foreign currency exchange rate fluctuations impact Amazon's net sales in 2024 according to Item 7, and what foreign currency sensitivities and foreign fund holdings were disclosed in Item 7A?",
        "target_sections": ["Item 7", "Item 7A"],
        "ground_truth_answer": "In Item 7, Amazon disclosed that changes in foreign exchange rates reduced consolidated net sales by $2.3 billion in 2024, with International segment net sales decreasing by $1.8 billion due to year-over-year currency movements. In Item 7A, Amazon reported holding $25.5 billion in foreign-denominated funds (cash, cash equivalents, and marketable securities) as of December 31, 2024, noting that hypothetical adverse currency changes of 5%, 10%, and 20% would result in fair value declines of $1.3 billion, $2.6 billion, and $5.1 billion, respectively.",
        "ground_truth_numbers": ["$2.3 billion", "$1.8 billion", "$25.5 billion", "5%", "10%", "20%", "$1.3 billion", "$2.6 billion", "$5.1 billion"],
    },
    {
        "id": "GOLD-41",
        "ticker": "GOOGL",
        "fiscal_years": [2024],
        "category": "cross_section_multihop",
        "min_required_hops": 2,
        "query": "What major European Commission antitrust fines and cash payments were disclosed in Note 10 of Alphabet's 2024 Form 10-K, and what were its future content licensing commitments?",
        "target_sections": ["Item 3", "Item 8 Note 10"],
        "ground_truth_answer": "In Note 10, Alphabet disclosed that in September 2024, the European Court of Justice upheld the EC's €2.4 billion Google Shopping fine, resulting in Alphabet making a $3.0 billion cash payment in Q3 2024. For the Android matter, the General Court affirmed a reduced fine of €4.1 billion (appealed and pending), following Alphabet's $5.1 billion charge recognized in 2018 (reduced by $217 million in 2022). Furthermore, Alphabet disclosed $8.8 billion in future fixed or minimum guaranteed content licensing commitments as of December 31, 2024, payable quarterly through Q1 2030.",
        "ground_truth_numbers": ["€2.4 billion", "$3.0 billion", "€4.1 billion", "$5.1 billion", "$217 million", "$8.8 billion", "2030"],
    },
    {
        "id": "GOLD-42",
        "ticker": "META",
        "fiscal_years": [2024],
        "category": "cross_section_multihop",
        "min_required_hops": 2,
        "query": "Compare the revenue and operating performance of Meta's Family of Apps versus Reality Labs in 2024 according to Item 7 and Note 15, and identify the primary operational drivers.",
        "target_sections": ["Item 7", "Item 8 Note 15"],
        "ground_truth_answer": "In 2024, Meta's Family of Apps (FoA) revenue rose 22% to $162,355 million (driven by a $28.68 billion increase in advertising revenue and an 11% increase in ad impressions), delivering operating income of $87,109 million (up 39% from $62,871 million in 2023). Conversely, Reality Labs generated $2,146 million in revenue but incurred an operating loss of $(17,729) million (widened from $(16,120) million in 2023) due to ongoing product development costs and employee compensation.",
        "ground_truth_numbers": ["$162,355 million", "22%", "$28.68 billion", "11%", "$87,109 million", "39%", "$2,146 million", "$(17,729) million", "$(16,120) million"],
    },
    {
        "id": "GOLD-43",
        "ticker": "TSLA",
        "fiscal_years": [2024],
        "category": "cross_section_multihop",
        "min_required_hops": 2,
        "query": "How did Tesla's automotive regulatory credits revenue change in 2024 according to Item 8 tables, and what specific factory disruptions were disclosed in Item 7 MD&A?",
        "target_sections": ["Item 7", "Item 8 Note 1"],
        "ground_truth_answer": "In Item 8 financial statement tables, Tesla disclosed that automotive regulatory credits revenue increased 54% to $2,763 million in 2024 from $1,790 million in 2023 (an increase of $973 million). In Item 7 MD&A, management disclosed that vehicle delivery and production growth was constrained by factory shutdowns at Gigafactory Berlin-Brandenburg caused by maritime shipping diversions from the Red Sea conflict and an arson attack, alongside factory retooling for the updated Model 3 and ramp of Cybertruck.",
        "ground_truth_numbers": ["$2,763 million", "$1,790 million", "$973 million", "54%"],
    },
    {
        "id": "GOLD-44",
        "ticker": "TSLA",
        "fiscal_years": [2024],
        "category": "cross_section_multihop",
        "min_required_hops": 2,
        "query": "What fee awards and legal proceedings were disclosed in Item 3 of Tesla's 2024 Form 10-K regarding the 2018 CEO Performance Award and Directors' Compensation litigation?",
        "target_sections": ["Item 3", "Item 8 Note on Commitments and Contingencies"],
        "ground_truth_answer": "In Item 3, Tesla disclosed that on January 30, 2024, the Delaware Court of Chancery rescinded Elon Musk's 2018 CEO Performance Award; after 72% of disinterested voting shares voted to ratify the award at the 2024 Annual Meeting, the court denied a motion to revise on December 2, 2024, and awarded plaintiff's counsel $345 million in fees (appealed to the Delaware Supreme Court). In the Directors' Compensation derivative lawsuit, the court approved a settlement on January 8, 2025, and awarded plaintiff's counsel approximately $176 million in fees, which Tesla announced it intends to appeal.",
        "ground_truth_numbers": ["January 30, 2024", "72%", "December 2, 2024", "$345 million", "January 8, 2025", "$176 million"],
    },
    {
        "id": "GOLD-45",
        "ticker": "JPM",
        "fiscal_years": [2024],
        "category": "cross_section_multihop",
        "min_required_hops": 2,
        "query": "What did JPMorgan Chase disclose in Item 7 regarding the drivers of net interest income in 2024, and what range of reasonably possible legal losses was disclosed in Note 30?",
        "target_sections": ["Item 7", "Item 8 Note 30"],
        "ground_truth_answer": "In Item 7, JPMorgan Chase explained that net interest income was driven by the higher interest rate environment and asset yields across its lending portfolios, tempered by rising deposit funding costs and deposit migration into higher-yielding CDs. In Note 30 (Litigation), the Firm estimated that the aggregate range of reasonably possible losses, in excess of established legal reserves, was from $0 to approximately $1.4 billion as of December 31, 2024.",
        "ground_truth_numbers": ["$0", "$1.4 billion", "December 31, 2024"],
    },
    {
        "id": "GOLD-46",
        "ticker": "JPM",
        "fiscal_years": [2024],
        "category": "cross_section_multihop",
        "min_required_hops": 2,
        "query": "How does JPMorgan Chase describe its legal proceedings in Item 3, and what accounting standard and judgment factors for litigation loss contingencies are disclosed in Note 30?",
        "target_sections": ["Item 3", "Item 8 Note 30"],
        "ground_truth_answer": "In Item 3, JPMorgan Chase directly refers to Note 30 for description of material legal proceedings. In Note 30, the Firm discloses that it establishes litigation reserves when a loss is probable and reasonably estimable, noting that determining loss ranges involves significant judgment due to evolving multi-defendant cases, unresolved class certifications, and novel legal theories across its business lines.",
        "ground_truth_numbers": [],
    },
    {
        "id": "GOLD-47",
        "ticker": "JNJ",
        "fiscal_years": [2024],
        "category": "cross_section_multihop",
        "min_required_hops": 2,
        "query": "What reserves and remaining payments were disclosed in Note 19 of Johnson & Johnson's 2024 Form 10-K for talc litigation matters and opioid settlement agreements?",
        "target_sections": ["Item 3", "Item 8 Note 19"],
        "ground_truth_answer": "In Note 19 (Legal Proceedings), Johnson & Johnson disclosed that operating cash flows will fund an approximately $11.6 billion ($13.5 billion nominal) reserve established for talc-related product liability matters, alongside an estimated remaining balance of approximately $1.5 billion to be paid under the nationwide agreement to settle opioid litigation.",
        "ground_truth_numbers": ["$11.6 billion", "$13.5 billion", "$1.5 billion"],
    },
    {
        "id": "GOLD-48",
        "ticker": "JNJ",
        "fiscal_years": [2024],
        "category": "cross_section_multihop",
        "min_required_hops": 2,
        "query": "How did worldwide sales perform across Innovative Medicine and MedTech in 2024 according to Note 17, and what gain was recognized on the Kenvue separation in Note 21?",
        "target_sections": ["Item 7", "Item 8 Note 17", "Item 8 Note 21"],
        "ground_truth_answer": "In Note 17, Johnson & Johnson reported worldwide Innovative Medicine sales of $56,964 million (up 4.0% from $54,759 million in 2023) and MedTech sales of $31,857 million (up 4.8% from $30,400 million in 2023), resulting in total enterprise sales of $88,821 million. In Note 21, the Company disclosed a pre-tax gain of $20,984 million recognized on the separation of Kenvue Inc. in 2023, which drove 2023 discontinued operations net earnings of $21,827 million.",
        "ground_truth_numbers": ["$56,964 million", "$54,759 million", "$31,857 million", "$30,400 million", "$88,821 million", "4.0%", "4.8%", "$20,984 million", "$21,827 million"],
    },
    {
        "id": "GOLD-49",
        "ticker": "WMT",
        "fiscal_years": [2025],
        "category": "cross_section_multihop",
        "min_required_hops": 2,
        "query": "What were the net sales and operating income for Walmart U.S. and Walmart International in FY2025 according to Note 12, and what omnichannel drivers were cited in Item 7?",
        "target_sections": ["Item 7", "Item 8 Note 12"],
        "ground_truth_answer": "In Note 12, Walmart reported that in FY2025 Walmart U.S. generated net sales of $462,415 million and operating income of $23,882 million (up from $441,817 million and $22,154 million in FY2024), while Walmart International generated net sales of $121,885 million and operating income of $5,501 million (up from $114,641 million and $4,909 million in FY2024). In Item 7 MD&A, management attributed this growth to strong eCommerce growth, store-fulfilled pickup and delivery, and expanding global marketplace advertising.",
        "ground_truth_numbers": ["$462,415 million", "$23,882 million", "$441,817 million", "$22,154 million", "$121,885 million", "$5,501 million", "$114,641 million", "$4,909 million"],
    },
    {
        "id": "GOLD-50",
        "ticker": "WMT",
        "fiscal_years": [2025],
        "category": "cross_section_multihop",
        "min_required_hops": 2,
        "query": "What ongoing legal proceedings and opioid-related litigation were disclosed in Item 3 and Note 10 of Walmart's FY2025 Form 10-K, including the multi-district litigation in Ohio?",
        "target_sections": ["Item 3", "Item 8 Note 10"],
        "ground_truth_answer": "In Item 3 and Note 10 (Contingencies), Walmart disclosed that it remains a defendant in approximately 250 cases in the multi-district litigation entitled In re National Prescription Opiate Litigation (MDL No. 2804) pending in the U.S. District Court for the Northern District of Ohio, alongside more than 25 other opioid cases and a DOJ lawsuit in Delaware, following its entry into a $3.1 billion nationwide opioid settlement framework. Walmart accrues liabilities when losses are probable and reasonably estimable but cannot estimate additional ranges of loss for unresolved claims.",
        "ground_truth_numbers": ["250", "2804", "$3.1 billion"],
    },
]


def validate_dataset(data: List[Dict[str, Any]]) -> None:
    """Validate completeness, uniqueness, schemas, and counts across tiers and tickers."""
    assert len(data) == 50, f"Expected 50 questions, got {len(data)}"

    expected_tickers = {"AAPL", "MSFT", "AMZN", "GOOGL", "META", "NVDA", "TSLA", "JPM", "JNJ", "WMT"}
    expected_categories = {"single_hop_factual", "quantitative_tabular", "cross_section_multihop"}
    required_keys = {
        "id",
        "ticker",
        "fiscal_years",
        "category",
        "min_required_hops",
        "query",
        "target_sections",
        "ground_truth_answer",
        "ground_truth_numbers",
    }

    from collections import Counter
    cat_counts = Counter(d["category"] for d in data)
    assert cat_counts["single_hop_factual"] == 15, f"Expected 15 single_hop_factual, got {cat_counts['single_hop_factual']}"
    assert cat_counts["quantitative_tabular"] == 20, f"Expected 20 quantitative_tabular, got {cat_counts['quantitative_tabular']}"
    assert cat_counts["cross_section_multihop"] == 15, f"Expected 15 cross_section_multihop, got {cat_counts['cross_section_multihop']}"

    ticker_counts = Counter(d["ticker"] for d in data)
    for t in expected_tickers:
        assert ticker_counts[t] == 5, f"Ticker {t} should have exactly 5 questions, got {ticker_counts[t]}"

    for i, item in enumerate(data):
        expected_id = f"GOLD-{i+1:02d}"
        assert item["id"] == expected_id, f"Item {i} id expected {expected_id}, got {item['id']}"
        assert set(item.keys()) == required_keys, f"Item {item['id']} keys mismatch: {set(item.keys())}"
        assert item["ticker"] in expected_tickers, f"Unknown ticker {item['ticker']}"
        assert item["category"] in expected_categories, f"Unknown category {item['category']}"
        assert isinstance(item["fiscal_years"], list) and len(item["fiscal_years"]) >= 1
        assert isinstance(item["target_sections"], list) and len(item["target_sections"]) >= 1
        assert len(item["query"]) > 15
        assert len(item["ground_truth_answer"]) > 20
        assert isinstance(item["ground_truth_numbers"], list)
        for num in item["ground_truth_numbers"]:
            assert num in item["ground_truth_answer"], f"Ground truth number '{num}' not found in answer for {item['id']}"


def main() -> None:
    validate_dataset(GOLDEN_QUESTIONS)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(GOLDEN_QUESTIONS, f, indent=2, ensure_ascii=False)
    print(f"Successfully generated and validated canonical 50-question golden eval benchmark at: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
