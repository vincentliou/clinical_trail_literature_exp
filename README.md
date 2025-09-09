# clinical_trail_literature_exp
Declaration: this is jut an experiment about how to use the openai API to parse a set of clinical literature.  Not for real-world clinical trail results analysis.

This script try to establish a workflow to understand up-to-date colorectal cancer clinical trials with antibody therapeutics. Here is the process for the search 
1.  In clinical trial .com, you can download a list of the clinical trials results. The current csv file was downloaded with using the following search query:
`metastatic colorectal cancer treatment OR advanced colorectal cancer treatment`
You can then refine the results on the ClinicalTrials.gov website using the following filters:
- **Status:** `Completed` (to find studies with results)
- **Phase:** `Phase 1`, `Phase 2`, `Phase 1/2`
- **Study Type:** `Interventional`
- **Purpose:** `Treatment`
Lesson: please be better to download the search query in the “advanced search”.
Outcome: colorectal_combine2.csv.

