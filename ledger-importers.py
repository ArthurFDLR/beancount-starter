import sys
from pathlib import Path

IMPORT_PATH = Path(__file__).resolve().parent / "importers"
sys.path.append(str(IMPORT_PATH))

from importer_template import GenericImporter


CONFIG = [
    GenericImporter(
        account='Assets:GenericBank:Checking',
        expenseCat='Expenses:FIXME',
        creditCat='Income:FIXME',
    ),
]

if __name__ == "__main__":
    import argparse
    from pathlib import Path
    import logging
    logging.basicConfig(level=logging.INFO)

    from beancount.ingest import identify
    from beancount.ingest import extract
    from beancount.ingest import file

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--statements",
        type=str,
        required=True,
        help="Path to the folder containing the statements",
    )
    parser.add_argument(
        "-o", "--output", type=str, required=True, help="Path to the output file"
    )
    parser.add_argument(
        "-d",
        "--documents",
        type=str,
        required=True,
        help="Path to the folder containing the documents",
    )
    parser.add_argument(
        "-r",
        "--reverse",
        "--descending",
        action="store_const",
        dest="ascending",
        default=True,
        const=False,
        help="Write out the entries in descending order",
    )
    parser.add_argument(
        "--no-overwrite",
        dest="overwrite",
        action="store_false",
        default=True,
        help="Don't overwrite destination files with the same name.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't actually move files, just print what would be done",
    )
    args = parser.parse_args()

    statement_path = Path(args.statements).resolve()
    output_path = Path(args.output).resolve()
    documents_path = Path(args.documents).resolve()

    if not statement_path.is_dir():
        parser.error(f"{statement_path} is not a directory")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not args.dry_run:
        documents_path.mkdir(parents=True, exist_ok=True)

    # Identify files
    logging.info("Identifying files...")
    identify.identify(
        importers_list=CONFIG,
        files_or_directories=[str(statement_path)],
    )
    logging.info("Files identification done.")

    # Prompt user to start the operations extraction
    logging.info("Press enter to proceed with operations extraction, or Ctrl+C to abort.")
    input()

    # Extract transactions
    logging.info("Extracting operations...")
    with open(output_path, "w") as ouput_file:
        extract.extract(
            importer_config=CONFIG,
            files_or_directories=[str(statement_path)],
            output=ouput_file,
            ascending=args.ascending,
            hooks=None,
        )
    logging.info("Operations extraction done.")

    # Prompt user to start the documents import\
    logging.info("Press enter to proceed with documents import, or Ctrl+C to abort.")
    input()

    # Move documents
    logging.info("Importing documents...")
    file.file(
        importer_config=CONFIG,
        files_or_directories=[str(statement_path)],
        destination=str(documents_path),
        mkdirs=True,
        idify=True,
        overwrite=args.overwrite,
        logfile=sys.stdout,
        dry_run=args.dry_run,
    )
    logging.info("Documents import done.")
