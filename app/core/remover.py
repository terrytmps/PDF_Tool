from PyPDF2 import PdfReader, PdfWriter
import os


class PdfPageRemover:
    def remove_pages(self, input_path, pages_to_remove, output_dir):
        """
        Supprime des pages spécifiques d'un PDF
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Fichier introuvable : {input_path}")

        pages = self._parse_page_ranges(pages_to_remove)
        output_path = self._generate_output_path(input_path, output_dir)

        try:
            with open(input_path, "rb") as file:
                reader = PdfReader(file)
                self._validate_page_numbers(reader, pages)

                writer = PdfWriter()
                for i in range(len(reader.pages)):
                    if (i + 1) not in pages:
                        writer.add_page(reader.pages[i])

                with open(output_path, "wb") as output_file:
                    writer.write(output_file)

            return output_path
        except Exception as e:
            raise RuntimeError(f"Échec de la suppression : {str(e)}")

    def _parse_page_ranges(self, page_ranges):
        pages = set()
        for part in page_ranges.replace(" ", "").split(","):
            if "-" in part:
                start, end = map(int, part.split("-"))
                pages.update(range(start, end + 1))
            else:
                pages.add(int(part))
        return pages

    def _generate_output_path(self, input_path, output_dir):
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        return os.path.join(output_dir, f"{base_name}_sans_pages.pdf")

    def _validate_page_numbers(self, reader, pages):
        total_pages = len(reader.pages)
        for page in pages:
            if page < 1 or page > total_pages:
                raise ValueError(
                    f"Numéro de page invalide : {page} (total pages: {total_pages})"
                )
