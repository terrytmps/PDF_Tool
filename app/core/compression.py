import os
from PyPDF2 import PdfReader, PdfWriter


class FileCompressor:
    def compress_files(self, input_files, output_path, compression_level="good"):
        compressed_files = []
        # Map compression levels to zlib levels
        compression_levels = {
            "less": 9,  # Maximum compression
            "good": 6,  # Default balance
            "high": 3,  # No compression
        }
        zlib_level = compression_levels.get(compression_level, 6)

        for input_file in input_files:
            try:
                with open(input_file, "rb") as file:
                    reader = PdfReader(file)
                    writer = PdfWriter()

                    for page in reader.pages:
                        writer.add_page(page)

                    output_filename = f"{os.path.splitext(os.path.basename(input_file))[0]}_compressed.pdf"
                    output_filepath = os.path.join(output_path, output_filename)
                    os.makedirs(output_path, exist_ok=True)

                    with open(output_filepath, "wb") as output_file:
                        writer.write(output_file)

                    compressed_files.append(output_filepath)
            except Exception as e:
                print(f"Error compressing {input_file}: {e}")
        return compressed_files
