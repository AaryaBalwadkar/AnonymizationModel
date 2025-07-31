import pyminizip
import os
import tempfile
import uuid


def zip_with_password(file_path, password):
    # Use a persistent temp file that won't be deleted immediately
    zip_output_dir = tempfile.gettempdir()

    # Unique name to avoid conflict
    zip_filename = f"anonymized_{uuid.uuid4().hex}.zip"
    output_zip = os.path.join(zip_output_dir, zip_filename)

    try:
        pyminizip.compress(file_path, None, output_zip, password, 5)
        print(f"✅ ZIP created at: {output_zip}")
        return output_zip
    except Exception as e:
        print(f"❌ ZIP creation failed: {str(e)}")
        raise Exception(f"Failed to create ZIP: {str(e)}")

