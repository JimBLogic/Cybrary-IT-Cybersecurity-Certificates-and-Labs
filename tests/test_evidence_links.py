"""Source-only integrity checks: never parse/upload the personal certificates."""
from datetime import date
from pathlib import Path
import re
import unittest
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")
ROWS = re.findall(
    r"^\|[^\n]*?\]\((\./(?:Certificates|Labs)/[^)]+)\)\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|",
    README, flags=re.MULTILINE,
)
EXPECTED = {"Certificates": 9, "Labs": 7}


def checked_path(value: str) -> Path:
    decoded = unquote(value)
    path = Path(decoded)
    if path.is_absolute() or ".." in path.parts or not decoded.startswith(("./Certificates/", "./Labs/")):
        raise ValueError("A linked certificate path escaped its expected folder")
    target = (ROOT / decoded).resolve()
    if not target.is_relative_to(ROOT) or target.is_symlink():
        raise ValueError("Certificate path escapes the archive")
    return target


class EvidenceTests(unittest.TestCase):
    def test_all_sixteen_claimed_certificate_and_lab_paths_exist(self):
        self.assertEqual(len(ROWS), sum(EXPECTED.values()))
        counts = {key: 0 for key in EXPECTED}
        for raw, category, _ in ROWS:
            target = checked_path(raw)
            self.assertTrue(target.is_file(), f"Missing evidence path: {raw}")
            self.assertEqual(target.suffix.lower(), ".pdf")
            self.assertGreater(target.stat().st_size, 1000, f"Placeholder evidence: {raw}")
            counts[category] += 1
        self.assertEqual(counts, EXPECTED)

    def test_no_unreviewed_orphan_pdfs_represented_as_completed_courses(self):
        claimed = {checked_path(row[0]) for row in ROWS}
        pdfs = {p.resolve() for sub in EXPECTED for p in (ROOT / sub).glob("*.pdf")}
        self.assertEqual(
            pdfs - claimed,
            {(ROOT / "Labs" / "cybrary-cert-welcome-to-cybrary.pdf").resolve()},
        )
        self.assertFalse(claimed - pdfs)

    def test_dates_are_iso_calendar_dates_not_future_dated(self):
        for path, _, date_text in ROWS:
            completed = date.fromisoformat(date_text)
            self.assertLessEqual(completed, date(2026, 10, 16), path)
        self.assertEqual(len(set(path for path, _, _ in ROWS)), len(ROWS))

    def test_public_claim_and_ci_permissions_remain_scoped(self):
        self.assertIn("does not imply", README)
        self.assertIn("does not include course solutions", README)
        workflow = (ROOT / ".github/workflows/evidence-links.yml").read_text(encoding="utf-8")
        self.assertIn("contents: read", workflow)
        self.assertIn("persist-credentials: false", workflow)
        self.assertIn("unittest discover", workflow)
        self.assertNotIn("contents: write", workflow)
        self.assertNotIn("workflow_dispatch", workflow)
        self.assertNotIn("deploy-pages", workflow)


if __name__ == "__main__":
    unittest.main()
