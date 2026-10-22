"""A sincronização que grava regenera a galeria; --check, --dry-run e --no-gallery não."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("sync_shared", ROOT / "_TOOLS/sync_shared.py")
SYNC = importlib.util.module_from_spec(spec)
spec.loader.exec_module(SYNC)


class SyncGalleryTests(unittest.TestCase):
    def run_sync(self, *args: str, gallery: subprocess.CompletedProcess | None = None) -> tuple[int, mock.Mock, str]:
        result = gallery or subprocess.CompletedProcess([], 0, stdout="OK index.html (18 entregáveis)\n", stderr="")
        output = io.StringIO()
        with mock.patch.object(SYNC, "actions", return_value=[]), \
                mock.patch.object(SYNC.subprocess, "run", return_value=result) as run, \
                mock.patch.object(sys, "argv", ["sync_shared.py", *args]), contextlib.redirect_stdout(output):
            code = SYNC.main()
        return code, run, output.getvalue()

    def test_write_mode_regenerates_gallery(self) -> None:
        code, run, output = self.run_sync()
        self.assertEqual(code, 0)
        run.assert_called_once()
        self.assertEqual(run.call_args.args[0][1], str(ROOT / "_GALERIA/gerar.py"))
        self.assertIn("18 entregáveis", output)

    def test_check_dry_run_and_opt_out_skip_gallery(self) -> None:
        for args in (["--check"], ["--dry-run"], ["--no-gallery"]):
            with self.subTest(args=args):
                code, run, _ = self.run_sync(*args)
                self.assertEqual(code, 0)
                run.assert_not_called()

    def test_gallery_failure_only_warns(self) -> None:
        failed = subprocess.CompletedProcess([], 1, stdout="", stderr="ModuleNotFoundError: reportlab\n")
        code, _, output = self.run_sync(gallery=failed)
        self.assertEqual(code, 0)
        self.assertIn("AVISO: galeria não gerada (ModuleNotFoundError: reportlab)", output)


if __name__ == "__main__":
    unittest.main()
