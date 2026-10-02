"""Tests for secrets.py: no network, no Keychain. Run with `python3 -m unittest` from the repo root.

A temp folder stands in for HOME, a small script stands in for `bws` (it serves secrets from a JSON file and
records edits), and token() is replaced so the Keychain is never read.
"""
from __future__ import annotations

import importlib.util
import io
import json
import os
import stat
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("mac_secrets", ROOT / "secrets.py")  # `secrets` is a stdlib name
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)

FAKE_BWS = """#!/usr/bin/env python3
import json, os, sys
db = os.environ["FAKE_BWS_DB"]
data = json.load(open(db))
a = [x for x in sys.argv[1:] if x not in ("--output", "json")]
# Like the real bws (clap): before "--", an argument starting with "-" is an option, and an unknown one
# is refused with an error that repeats it.
if "--" in a:
    i = a.index("--"); head, tail = a[:i], a[i + 1:]
else:
    head, tail = a, []
out, j = [], 0
while j < len(head):
    x = head[j]
    if x == "--value" and j + 1 < len(head) and not head[j + 1].startswith("-"):
        out += ["--value", head[j + 1]]; j += 2; continue
    if x.startswith("--value="):
        out += ["--value", x[len("--value="):]]; j += 1; continue
    if x.startswith("-"):
        sys.exit("error: unexpected argument '" + x + "' found")
    out.append(x); j += 1
a = out + tail
if a[:2] == ["project", "list"]:
    print(json.dumps([{"id": "p1", "name": "personal-agent"}]))
elif a[:2] == ["secret", "list"]:
    print(json.dumps([{"id": k, "key": k, "value": v} for k, v in data.items()]))
elif a[:2] == ["secret", "edit"]:
    rest = a[2:]; v = rest.index("--value"); value = rest[v + 1]; del rest[v:v + 2]
    data[rest[0]] = value; json.dump(data, open(db, "w")); print("{}")
elif a[:2] == ["secret", "create"]:
    data[a[2]] = a[3]; json.dump(data, open(db, "w")); print("{}")
else:
    sys.exit("unexpected: " + " ".join(a))
"""


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name) / "home"
        (self.home / "Projects").mkdir(parents=True)
        self.outside = Path(self.tmp.name) / "outside"
        self.outside.mkdir()
        fake = Path(self.tmp.name) / "bws"
        fake.write_text(FAKE_BWS)
        fake.chmod(0o755)
        self.db = Path(self.tmp.name) / "db.json"
        self.set_secrets({})
        patches = [
            mock.patch.dict(os.environ, {"HOME": str(self.home), "FAKE_BWS_DB": str(self.db)}),
            mock.patch.object(S, "BWS", str(fake)),
            mock.patch.object(S, "token", lambda write=False: "fake-token"),
        ]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)
        self.addCleanup(self.tmp.cleanup)

    def set_secrets(self, d):
        self.db.write_text(json.dumps(d))

    def stored(self):
        return json.loads(self.db.read_text())

    def run_cmd(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = S.main(list(argv))
        return code, out.getvalue(), err.getvalue()


class NamesAndQuoting(unittest.TestCase):
    def test_name_pattern(self):
        for ok in ("A", "_X", "API_KEY_2"):
            self.assertTrue(S.NAME_RE.match(ok), ok)
        for bad in ("a", "1A", "A-B", "A;rm -rf ~", "A B", "", "A\n"):
            self.assertFalse(S.NAME_RE.match(bad), bad)

    def test_unquote_stored(self):
        self.assertEqual(S.unquote_stored('"abc"'), "abc")
        self.assertEqual(S.unquote_stored("'a b'"), "a b")
        self.assertEqual(S.unquote_stored("""'it'"'"'s'"""), "it's")
        self.assertEqual(S.unquote_stored("abc"), "abc")            # raw values stay raw
        self.assertEqual(S.unquote_stored('"a" "b"'), '"a" "b"')    # two words: not one quoted word
        self.assertEqual(S.unquote_stored("'unbalanced"), "'unbalanced")
        self.assertEqual(S.unquote_stored("x'y'"), "x'y'")

    def test_zshrc_text_quotes_and_refuses(self):
        text, refused = S.zshrc_text({"OK": "a b; $(touch pwned) `x`", "OLD": '"legacy"', "bad;name": "v"})
        self.assertEqual(refused, ["bad;name"])
        self.assertIn("export OK='a b; $(touch pwned) `x`'\n", text)
        self.assertIn("export OLD=legacy\n", text)
        self.assertNotIn("bad", text)

    def test_written_file_is_inert_in_a_shell(self):
        import subprocess
        evil = "x'; touch PWNED; '$(touch PWNED2)"
        text, _ = S.zshrc_text({"EVIL": evil})
        with tempfile.TemporaryDirectory() as d:
            r = subprocess.run(["/bin/sh", "-c", text + 'printf %s "$EVIL"'], cwd=d, capture_output=True, text=True)
            self.assertEqual(r.stdout, evil)
            self.assertEqual(os.listdir(d), [])

    def test_parse_export(self):
        self.assertEqual(S.parse_export("export A=plain"), ("A", "plain"))
        self.assertEqual(S.parse_export('export A="quoted value"  # note'), ("A", "quoted value"))
        self.assertEqual(S.parse_export("export A='$literal'"), ("A", "$literal"))
        self.assertEqual(S.parse_export("export A="), ("A", ""))
        self.assertIsNone(S.parse_export("# comment"))
        for bad in ("export lower=x", 'export A="$HOME/x"', "export A=$(id)", "export A=a b", "export A='open",
                    """export A="'quoted'" """):
            with self.assertRaises(ValueError, msg=bad):
                S.parse_export(bad)

    def test_round_trip(self):
        for v in ("plain", "with space", "it's", 'dq"in', "$no_expand", "", "back\\slash"):
            text, _ = S.zshrc_text({"V": v})
            self.assertEqual(S.parse_export(text.splitlines()[-1]), ("V", v))


class Destinations(Base):
    def ok(self, p):
        path, why = S.destination(p)
        self.assertIsNotNone(path, f"{p}: {why}")

    def refused(self, p):
        path, why = S.destination(p)
        self.assertIsNone(path, p)
        return why

    def test_allowed(self):
        (self.home / "Projects/app").mkdir()
        for p in ("~/.config/mac-setup/repos.txt", "~/.config/a/b/c", "~/.eight-sleep-mcp/config.json",
                  "~/.ssh/config", "~/Projects/app/.env", "~/Projects/app/.env.prod"):
            self.ok(p)

    def test_refused(self):
        for p in ("~/.zshrc", "~/.zshrc.local", "~/.zprofile", "~/.ssh/authorized_keys", "~/.ssh/id_ed25519",
                  "~/Library/LaunchAgents/x.plist", "~/.config", "~/.eight-sleep-mcp", "~/Projects/.env",
                  "~/Projects/app/sub/.env", "~/Projects/app/env", "~/Projects/app/.envrc",
                  "~/.config/../.zshrc", "~/./.ssh/config", "~//.ssh/config", "/etc/hosts", "~/.config/x/",
                  "relative/.env"):
            self.refused(p)

    def test_symlinked_parent_escape(self):
        (self.home / ".config").symlink_to(self.outside)
        self.assertIn("outside the home", self.refused("~/.config/x/secret"))

    def test_symlinked_parent_inside_home_but_not_allowed(self):
        (self.home / "Library").mkdir()
        (self.home / ".config").symlink_to(self.home / "Library")
        self.assertIn("isn't allowed", self.refused("~/.config/LaunchAgents/x.plist"))

    def test_symlinked_project(self):
        (self.home / "Projects/app").symlink_to(self.outside)
        self.refused("~/Projects/app/.env")

    def test_symlink_file_outside(self):
        (self.home / ".ssh").mkdir()
        (self.home / ".ssh/config").symlink_to(self.home / ".zshrc")
        self.refused("~/.ssh/config")

    def test_symlink_file_inside_allowlist(self):
        (self.home / ".config/a").mkdir(parents=True)
        (self.home / ".config/a/real").write_text("x")
        (self.home / ".config/a/link").symlink_to(self.home / ".config/a/real")
        self.ok("~/.config/a/link")


class Pull(Base):
    def test_pull_writes_quoted_env_and_allowed_files(self):
        (self.home / "Projects/app").mkdir()
        self.set_secrets({"env:TOKEN": '"abc def"', "env:RAW": "x$(id)", "env:bad-name": "v",
                          "file:~/.config/t/a.json": "{}", "file:~/Projects/app/.env": "K=V\n",
                          "file:~/Projects/missing/.env": "K=V\n", "file:~/.zshrc": "evil",
                          "file:~/Library/LaunchAgents/evil.plist": "evil"})
        code, out, err = self.run_cmd("pull")
        self.assertEqual(code, 1)
        z = (self.home / ".zshrc.local").read_text()
        self.assertIn("export TOKEN='abc def'\n", z)
        self.assertIn("export RAW='x$(id)'\n", z)
        self.assertNotIn("bad-name", z)
        self.assertEqual((self.home / ".config/t/a.json").read_text(), "{}")
        self.assertEqual(stat.S_IMODE((self.home / ".config/t/a.json").stat().st_mode), 0o600)
        self.assertEqual((self.home / "Projects/app/.env").read_text(), "K=V\n")
        self.assertIn("skipped  ~/Projects/missing/.env", out)
        self.assertFalse((self.home / ".zshrc").exists())
        self.assertFalse((self.home / "Library").exists())
        for k in ("env:bad-name", "file:~/.zshrc", "file:~/Library/LaunchAgents/evil.plist"):
            self.assertIn(f"refused  {k}", err)

    def test_check_reports_refusals_and_writes_nothing(self):
        self.set_secrets({"env:A": "1", "file:~/.config/x": "y", "file:~/.ssh/authorized_keys": "k"})
        for flag in ("--check", "--dry-run"):
            code, out, err = self.run_cmd("pull", flag)
            self.assertEqual(code, 1)
            self.assertIn("create   ~/.zshrc.local", out)
            self.assertIn("create   ~/.config/x", out)
            self.assertIn("refused  file:~/.ssh/authorized_keys", err)
            self.assertEqual(sorted(os.listdir(self.home)), ["Projects"])

    def test_pull_never_follows_symlink_outside(self):
        target = self.outside / "victim"
        target.write_text("original")
        (self.home / ".ssh").mkdir()
        (self.home / ".ssh/config").symlink_to(target)
        self.set_secrets({"file:~/.ssh/config": "Host *\n"})
        code, _, err = self.run_cmd("pull")
        self.assertEqual(code, 1)
        self.assertEqual(target.read_text(), "original")
        self.assertTrue((self.home / ".ssh/config").is_symlink())
        self.assertIn("refused", err)

    def test_pull_replaces_symlink_inside_allowlist(self):
        (self.home / ".config/a").mkdir(parents=True)
        real = self.home / ".config/a/real"
        real.write_text("old")
        (self.home / ".config/a/link").symlink_to(real)
        self.set_secrets({"file:~/.config/a/link": "new"})
        code, out, _ = self.run_cmd("pull")
        self.assertEqual(code, 0)
        self.assertFalse((self.home / ".config/a/link").is_symlink())
        self.assertEqual((self.home / ".config/a/link").read_text(), "new")
        self.assertEqual(real.read_text(), "old")
        self.assertEqual(self.run_cmd("pull")[1].strip(), "same     ~/.config/a/link")

    def test_clean_pull_exits_zero(self):
        self.set_secrets({"env:A": "1"})
        self.assertEqual(self.run_cmd("pull")[0], 0)


class Push(Base):
    def test_push_env_stores_unquoted(self):
        src = self.home / "env"
        src.write_text("export A=\"quoted\"\nexport B='x y' # note\nexport C=plain\nexport d=lower\n"
                       "export E=\"$HOME\"\n# export F=commented\n")
        self.set_secrets({"env:A": '"quoted"'})
        code, out, err = self.run_cmd("push-env", str(src))
        self.assertEqual(code, 1)
        self.assertEqual(self.stored(), {"env:A": "quoted", "env:B": "x y", "env:C": "plain"})
        self.assertIn("updated  env:A", out)
        self.assertIn("refused  d:", err)
        self.assertIn("refused  E:", err)

    def test_pull_then_push_is_stable(self):
        self.set_secrets({"env:A": "'v 1'", "env:B": "it's"})
        self.run_cmd("pull")
        self.run_cmd("push-env")
        self.assertEqual(self.stored(), {"env:A": "v 1", "env:B": "it's"})
        _, out, _ = self.run_cmd("push-env")
        self.assertEqual(out.split(), ["same", "env:A", "same", "env:B"])

    def test_push_file_pem_key(self):
        pem = "-----BEGIN PRIVATE KEY-----\nabc\n-----END PRIVATE KEY-----\n"
        (self.home / ".config/x").mkdir(parents=True)
        (self.home / ".config/x/k.p8").write_text(pem)
        code, _, _ = self.run_cmd("push-file", str(self.home / ".config/x/k.p8"))
        self.assertEqual(code, 0)
        (self.home / ".config/x/k.p8").write_text("-" + pem)   # edit path too
        code, _, _ = self.run_cmd("push-file", str(self.home / ".config/x/k.p8"))
        self.assertEqual(code, 0)
        self.assertEqual(self.stored(), {"file:~/.config/x/k.p8": "-" + pem})

    def test_bws_errors_never_show_values(self):
        with self.assertRaises(SystemExit) as e:
            S.bws("secret", "create", "k", "-----BEGIN topsecret", "p1", write=True, secret="-----BEGIN topsecret")
        self.assertNotIn("topsecret", str(e.exception))

    def test_bws_errors_hide_short_and_bare_values_but_keep_names(self):
        # The fake echoes every argument for an unknown command, like an error that prints the value bare.
        for value in ("abc", "line one\nline two"):
            with self.assertRaises(SystemExit) as e:
                S.bws("secret", "bogus", "env:MY_KEY", f"--value={value}", write=True, secret=value)
            msg = str(e.exception)
            self.assertIn("env:MY_KEY", msg)
            for piece in [value, *value.splitlines()]:
                self.assertNotIn(piece, msg)

    def test_push_file_allowlist(self):
        (self.home / ".config/x").mkdir(parents=True)
        (self.home / ".config/x/f").write_text("data")
        (self.home / ".zshrc").write_text("rc")
        code, _, err = self.run_cmd("push-file", str(self.home / ".zshrc"))
        self.assertEqual(code, 1)
        self.assertIn("refused", err)
        self.assertEqual(self.stored(), {})
        code, out, _ = self.run_cmd("push-file", str(self.home / ".config/x/f"))
        self.assertEqual(code, 0)
        self.assertEqual(self.stored(), {"file:~/.config/x/f": "data"})


class Tokens(unittest.TestCase):
    def setUp(self):
        S.token.cache_clear()
        self.addCleanup(S.token.cache_clear)

    def test_read_prefers_read_only_token(self):
        calls = []
        def kc(service):
            calls.append(service)
            return {"bws-access-token-read": "R", "bws-access-token": "W"}.get(service)
        with mock.patch.object(S, "_keychain", kc):
            self.assertEqual(S.token(), "R")
            self.assertEqual(S.token(write=True), "W")
        self.assertEqual(calls, ["bws-access-token-read", "bws-access-token"])

    def test_read_falls_back_and_caches(self):
        calls = []
        def kc(service):
            calls.append(service)
            return "W" if service == "bws-access-token" else None
        with mock.patch.object(S, "_keychain", kc):
            self.assertEqual(S.token(), "W")
            self.assertEqual(S.token(), "W")
        self.assertEqual(calls, ["bws-access-token-read", "bws-access-token"])

    def test_write_never_uses_read_token(self):
        with mock.patch.object(S, "_keychain", lambda s: "R" if s == "bws-access-token-read" else None):
            with self.assertRaises(SystemExit):
                S.token(write=True)


if __name__ == "__main__":
    unittest.main()
