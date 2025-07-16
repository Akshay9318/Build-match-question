import json
import shutil
import zipfile
from pathlib import Path

# 1. Configuration
PACKAGE_NAME = "match-material-role"
OUTPUT_FILE  = f"{PACKAGE_NAME}.h5p"
PKG_DIR      = Path("pkg")
CONTENT_DIR  = PKG_DIR / "content"

# 2. h5p.json (metadata at package root)
h5p_json = {
    "title": "Material to Role Matching",
    "mainLibrary": "H5P.QuestionSet",
    "license": "U",
    "author": "Your Name",
    "year": 2025,
    "changes": [],
    "majorVersion": 1,
    "minorVersion": 18,
    "patchVersion": 0
}

# 3. content/content.json (the single matching question)
content_json = {
    "questions": [
        {
            "question": {
                "library": "H5P.Matching 1.16",
                "params": {
                    "question": "Match each material to its primary role.",
                    "matches": [
                        {"id": "m1", "text": "CaO source"},
                        {"id": "m2", "text": "Source of SiO₂, Al₂O₃, Fe₂O₃"},
                        {"id": "m3", "text": "Controls setting time"},
                        {"id": "m4", "text": "Iron & alumina corrective"}
                    ],
                    "setOfMatches": [
                        {
                            "matches": ["m1", "m2", "m3", "m4"],
                            "elements": [
                                {"value": "Limestone",           "allowedMatches": ["m1"]},
                                {"value": "Clay & Shale",         "allowedMatches": ["m2"]},
                                {"value": "Gypsum",               "allowedMatches": ["m3"]},
                                {"value": "Laterite & Bauxite",   "allowedMatches": ["m4"]}
                            ]
                        }
                    ]
                }
            }
        }
    ],
    "behaviour": {
        "enableSolutionsButton": True,
        "enableRetry": True
    }
}

def build_h5p():
    # Clean up previous runs
    if PKG_DIR.exists():
        shutil.rmtree(PKG_DIR)
    CONTENT_DIR.mkdir(parents=True)

    # Write h5p.json
    (PKG_DIR / "h5p.json").write_text(
        json.dumps(h5p_json, indent=2), encoding="utf-8"
    )

    # Write content/content.json
    (CONTENT_DIR / "content.json").write_text(
        json.dumps(content_json, indent=2), encoding="utf-8"
    )

    # Package into .h5p (zip and rename)
    with zipfile.ZipFile(OUTPUT_FILE, "w", zipfile.ZIP_DEFLATED) as z:
        for folder, _, files in os.walk(PKG_DIR):
            for fn in files:
                fp = Path(folder) / fn
                # preserve the pkg root structure
                arcname = fp.relative_to(PKG_DIR)
                z.write(fp, arcname)

    print(f"✅ Built {OUTPUT_FILE}")

if __name__ == "__main__":
    import os
    build_h5p()