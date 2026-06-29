import json
import re


def extract_json(
    text: str
):

    if text is None:

        raise Exception(
            "Empty response received."
        )

    text = (
        text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    # -------------------------
    # Direct Parse
    # -------------------------

    try:

        return json.loads(
            text
        )

    except Exception:

        pass

    # -------------------------
    # JSON Object Extraction
    # -------------------------

    object_match = re.search(
        r"\{[\s\S]*\}",
        text
    )

    if object_match:

        try:

            return json.loads(
                object_match.group()
            )

        except Exception:

            pass

    # -------------------------
    # JSON Array Extraction
    # -------------------------

    array_match = re.search(
        r"\[[\s\S]*\]",
        text
    )

    if array_match:

        try:

            return json.loads(
                array_match.group()
            )

        except Exception:

            pass

    raise Exception(
        "No valid JSON found."
    )