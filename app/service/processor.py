import pandas as pd
from app.service.anonymizer import detect_pii
from app.service.redactor import apply_redaction
import tempfile
import os
import uuid


def process_file(file_bytes, filename, limit_rows=None):
    ext = filename.split(".")[-1].lower()
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, filename)
        with open(input_path, "wb") as f:
            f.write(file_bytes)

        if ext == "csv":
            df = pd.read_csv(input_path)
        elif ext == "json":
            df = pd.read_json(input_path)
        else:
            raise ValueError("Unsupported format")

        if limit_rows:
            df = df.head(limit_rows)

        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].astype(str).apply(
                    lambda x: apply_redaction(x, detect_pii(x), method="pseudonym")
                )

        output_path = os.path.join(tmpdir, "anonymized.csv")
        df.to_csv(output_path, index=False)

        # Copy the file to persistent location before tmpdir is deleted
        final_path = os.path.join(tempfile.gettempdir(), f"anonymized_{uuid.uuid4().hex}.csv")
        df.to_csv(final_path, index=False)

        return final_path
