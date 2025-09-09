# This script is a combination of dissect literature from clinical report
# while put structure information together
import sys
print(sys.executable)

#%%%
# version4: batch process all literature PDFs into CSV
from dotenv import load_dotenv
import os
import json
import pandas as pd
from pdf2image import convert_from_path
import pytesseract
from PyPDF2 import PdfReader
from openai import OpenAI

# --- Setup ---
#version2: use .env file
load_dotenv()  # Load environment variables from .env file
API_KEY_PATH = os.getenv("API_KEY_PATH")
output_dir = os.getenv("output_dir")



with open(API_KEY_PATH) as f:
    api_key = f.read().strip()

os.environ["OPENAI_API_KEY"] = api_key
client = OpenAI()

literature_test_dir = os.getenv("literature_test_dir") 
output_csv = "trial_summary_literature_test.csv"

# --- Schema ---
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

# --- Helper: extract text from PDF ---
def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = "\n".join([page.extract_text() or "" for page in reader.pages])
    except Exception:
        text = ""

    # Fallback: OCR if text is empty
    if not text.strip():
        try:
            pages = convert_from_path(pdf_path)
            ocr_text = ""
            for i, page in enumerate(pages):
                ocr_text += pytesseract.image_to_string(page)
            text = ocr_text
        except Exception as e:
            print(f"OCR failed for {pdf_path}: {e}")
            text = ""

    return text

# --- Main processing loop ---
results = []
for fname in os.listdir(literature_test_dir):
    if not fname.lower().endswith(".pdf"):
        continue

    pdf_path = os.path.join(literature_test_dir, fname)
    nct_id = fname.split("_")[0]  # e.g., NCTxxxxxx from filename
    print(f"Processing {fname} ...")

    pdf_text = extract_text_from_pdf(pdf_path)

    # Ask OpenAI
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a clinical trial analyst. Use ONLY the text below."
                    "If information is missing, answer 'N/A'. Return JSON only. "
                    "Do not use any external or online content."
                )
            },
            {"role": "user",
             "content": f"Document:\n{pdf_text}\n\nNow extract into this schema:\n{json.dumps(schema, indent=2)}"}
        ],
        temperature=0
    )

    output_text = response.choices[0].message.content
    try:
        trial_json = json.loads(output_text)
    except json.JSONDecodeError:
        start = output_text.find("{")
        end = output_text.rfind("}") + 1
        trial_json = json.loads(output_text[start:end])

    trial_json["NCT_ID"] = nct_id
    results.append(trial_json)

# --- Save results to CSV ---
df = pd.DataFrame(results)
df.to_csv(output_csv, index=False)

print(f"✅ Saved {output_csv} with {len(results)} trials")


#%%%