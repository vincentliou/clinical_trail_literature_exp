# clinical_trail_literature_exp
Declaration: this is jut an experiment about how to use the openai API to parse a set of clinical literature.  Not for real-world clinical trail results analysis.

This script uses gpt-4o model.

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

export PATH=~/anaconda3/bin:$PATH

python -m venv docking

source docking/bin/activate
then you do this to install
pip install python-dotenv pandas pytesseract pdf2image PyPDF2 openai pytesseract

You need to have openai key.

This is the schema:
# -- Schema ---

schema = {
"NCT_ID": "Clinical trial identifier (e.g., NCTxxxxxx).",
"target_drug": "Name of the drug being studied.",
"phase": "Phase of the clinical trial (1, 2, 2a, 2b, 3).",
"regulatory_pathway": "Regulatory pathway: accelerated approval, breakthrough therapy, EUA, Fast track, priority review.",
"rationale": "What was the sponsor’s rationale for running the study?",
"bar_for_success": "Likely bar for success at the outset of the trial.",
"patient_selection_criteria": "How were patients identified, included, and excluded, and why?",
"validation_of_tests": "How well validated are the tests or biomarkers used to define the patient population?",
"study_design": "Describe the study design. Were the comparator and treatment length appropriate? Any special design features (run-in, crossover, interim analysis)?",
"primary_endpoint": "What were the endpoints, which was the primary one, how were they measured, and what is their relevance?",
"secondary_endpoint": "Secondary endpoints defined in the study.",
"effect_size": "What effect size was the trial designed to detect in the primary endpoint, and why?",
"design_implication": "How might the study design affect its ability to inform further development, approval, pricing, or market access?",
"enrollment_and_dropouts": "How many (in %) enrolled patients completed or dropped out, at what point, and why?",
"subject_characteristics": "What were the participant characteristics? Were arms balanced for key features?",
"analysis": "Did the analysis include all enrollments? If not, which patients were excluded and why?",
"sub_group": "How and why were sub-groups chosen? Pre-specified or post-hoc?",
"significance": "Were the drug effects statistically significant? Caveats?",
"safety": "Safety and tolerability findings.",
"consistency_and_plausibility": "Were results consistent and plausible across subgroups?",
"perception_of_finding": "Did the study meet sponsor goals? How might results be perceived by consumers?"
}

You can find the output here. 
