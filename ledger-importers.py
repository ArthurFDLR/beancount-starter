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