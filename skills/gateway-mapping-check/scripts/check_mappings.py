#!/usr/bin/env python3
"""Check that Spring controller endpoints are covered by an apiGateway path mapping.

Portable version: repo root is discovered via `git rev-parse --show-toplevel`, and
per-project paths (values.yaml, controllers glob, application.yml) come from
`.gateway-mapping-check.yaml` at the repo root, with CLI overrides and defaults.

Default mode inspects only controllers touched on the current branch (vs a base
ref), which is what you want before opening a PR. Use --all to audit every controller.

Exit code is 1 when any endpoint has no covering mapping, so this can gate a
pre-push hook or CI.
"""
import argparse
import re
import subprocess
import sys
from fnmatch import fnmatch
from pathlib import Path

# ---- defaults; overridable via .gateway-mapping-check.yaml or CLI flags ----
DEFAULTS = {
    "values_yaml": "chart/checkout/values.yaml",
    "application_yml": "src/main/resources/application.yml",
    "controllers_glob": "src/main/java/**/*Controller.java",
}
CONFIG_FILE = ".gateway-mapping-check.yaml"

METHOD_ANNOT = re.compile(r"@(Get|Post|Put|Delete|Patch)Mapping\b\s*(?:\(([^)]*)\))?")
CLASS_REQ_MAPPING = re.compile(r"@RequestMapping\s*\(([^)]*)\)", re.S)
STRING_LITERAL = re.compile(r'"([^"]*)"')
VALUE_OR_PATH = re.compile(r"(?:value|path)\s*=\s*\"([^\"]*)\"")
PLACEHOLDER = re.compile(r"\$\{([^}]+)\}")


# ----- repo & config --------------------------------------------------------

def find_repo():
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        return Path(out)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def load_config(repo):
    """Read .gateway-mapping-check.yaml (tiny hand-rolled parser, no PyYAML dep)."""
    cfg = dict(DEFAULTS)
    path = repo / CONFIG_FILE
    if not path.exists():
        return cfg
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, _, val = line.partition(":")
        key, val = key.strip(), val.strip().strip('"\'')
        if key in cfg and val:
            cfg[key] = val
    return cfg


# ----- application.yml placeholder parsing ---------------------------------

def load_placeholder_props(application_yml):
    """Resolve Spring base-path placeholders used in class-level @RequestMapping."""
    props = {
        "spring.data.rest.base-path.v1": "/api/v1",
        "spring.data.rest.base-path.v2": "/api/v2",
    }
    try:
        text = Path(application_yml).read_text(encoding="utf-8")
    except OSError:
        return props
    in_block = False
    for line in text.splitlines():
        if re.match(r"\s*base-path:\s*$", line):
            in_block = True
            continue
        if in_block:
            m = re.match(r"\s+(v\d+):\s*(\S+)", line)
            if m:
                props[f"spring.data.rest.base-path.{m.group(1)}"] = m.group(2)
            elif line.strip() and not line.startswith((" ", "\t")):
                in_block = False
    return props


def resolve_placeholders(path, props):
    def repl(m):
        key = m.group(1).split(":", 1)[0]
        return props.get(key, m.group(0))
    return PLACEHOLDER.sub(repl, path)


# ----- values.yaml parsing --------------------------------------------------

def load_gateway_mappings(values_yaml):
    text = Path(values_yaml).read_text(encoding="utf-8")
    m = re.search(r"apiPathComponent:\s*(\S+)", text)
    api_prefix = (m.group(1) if m else "/api/").rstrip("/")
    paths = re.findall(r"-\s*path:\s*(\S+)", text)
    return api_prefix, [p.strip().rstrip("/") or "/" for p in paths]


# ----- endpoint extraction --------------------------------------------------

def extract_path_literal(args):
    if not args:
        return ""
    m = VALUE_OR_PATH.search(args)
    if m:
        return m.group(1)
    for lit in STRING_LITERAL.findall(args):
        if lit.startswith("/") or lit.startswith("${"):
            return lit
    return ""


def class_base_path(text, props):
    class_idx = text.find(" class ")
    for m in CLASS_REQ_MAPPING.finditer(text):
        if class_idx != -1 and m.start() > class_idx:
            break
        base = extract_path_literal(m.group(1))
        if base:
            return resolve_placeholders(base, props)
    return ""


def join_paths(base, sub):
    full = "/" + base.strip("/")
    sub = sub.strip()
    if sub:
        full = full.rstrip("/") + "/" + sub.strip("/")
    full = re.sub(r"/{2,}", "/", full)
    return full.rstrip("/") or "/"


def strip_api_prefix(full, api_prefix):
    if full == api_prefix:
        return "/"
    if full.startswith(api_prefix + "/"):
        return full[len(api_prefix):]
    return full


def endpoints_in_file(path, props):
    text = Path(path).read_text(encoding="utf-8")
    base = class_base_path(text, props)
    out = []
    for m in METHOD_ANNOT.finditer(text):
        sub = extract_path_literal(m.group(2) or "")
        out.append((m.group(1).upper(), join_paths(base, sub)))
    return out


# ----- coverage -------------------------------------------------------------

def area(path):
    segs = [s for s in path.split("/") if s][:2]
    return "/" + "/".join(segs) if segs else "/"


def coverage(stripped, mappings, managed_areas):
    if stripped in mappings:
        return "exact", stripped
    prefixes = [p for p in mappings if p != "/" and stripped.startswith(p)]
    if prefixes:
        return "prefix", max(prefixes, key=len)
    if area(stripped) not in managed_areas:
        return "unmanaged", None
    return "missing", None


# ----- git ------------------------------------------------------------------

def git(repo, args):
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True).stdout


def resolve_base(repo, base):
    for ref in ([base] if base else ["origin/master", "master", "origin/main", "main", "HEAD~1"]):
        if ref and git(repo, ["rev-parse", "--verify", "--quiet", ref]).strip():
            return ref
    return None


def changed_controller_files(repo, base_ref, glob_pat):
    names = git(repo, ["diff", "--name-only", base_ref]).splitlines()
    return [n for n in names if fnmatch(n, glob_pat)]


def changed_endpoints(repo, base_ref, props, glob_pat):
    """Scan every controller file touched on the branch with the same extractor
    used by --all. Simpler and more robust than parsing diff hunks: multi-line
    annotations are handled, and endpoints whose mapping was removed from
    values.yaml still get re-checked. Pre-existing endpoints in a touched file
    show up too, but they report as exact/prefix, so the noise is minimal."""
    result = {}
    for rel in changed_controller_files(repo, base_ref, glob_pat):
        f = repo / rel
        if not f.exists():
            continue
        eps = endpoints_in_file(f, props)
        if eps:
            result[rel] = eps
    return result


# ----- reporting ------------------------------------------------------------

ICON = {"exact": "✅", "prefix": "🟡", "missing": "❌", "unmanaged": "ℹ️ "}


def report(groups, api_prefix, mappings, values_yaml_rel):
    managed_areas = {area(p) for p in mappings if p != "/"}
    missing = unmanaged = 0
    for rel, eps in sorted(groups.items()):
        print(f"\n{rel}")
        for method, full in eps:
            stripped = strip_api_prefix(full, api_prefix)
            status, cover = coverage(stripped, mappings, managed_areas)
            if status == "missing":
                missing += 1
                print(f"  {ICON[status]} {method:6} {full}  -> NO MAPPING for {stripped}")
            elif status == "prefix":
                print(f"  {ICON[status]} {method:6} {full}  -> covered by prefix '{cover}' (no dedicated entry)")
            elif status == "unmanaged":
                unmanaged += 1
                print(f"  {ICON[status]}{method:6} {full}  -> area '{area(stripped)}' is not gateway-managed (likely internal/admin)")
            else:
                print(f"  {ICON[status]} {method:6} {full}  -> '{cover}'")
    print()
    if unmanaged:
        print(f"ℹ️  {unmanaged} endpoint(s) in areas with no gateway mappings — confirm they are intentionally internal.")
    if missing:
        print(f"❌ {missing} endpoint(s) without a gateway mapping. "
              f"Add a '- path: <stripped-path>' entry under app.apiGateway.mappings in\n   {values_yaml_rel}")
    else:
        print("✅ All checked endpoints in gateway-managed areas are covered.")
    return missing


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--all", action="store_true", help="Audit every controller, not just changed ones.")
    ap.add_argument("--base", help="Base git ref to diff against (default: origin/master, master, main, HEAD~1).")
    ap.add_argument("--files", nargs="*", help="Explicit controller files to check.")
    ap.add_argument("--values-yaml", help=f"Path to Helm values.yaml (default from config or '{DEFAULTS['values_yaml']}').")
    ap.add_argument("--application-yml", help=f"Path to application.yml (default from config or '{DEFAULTS['application_yml']}').")
    ap.add_argument("--controllers-glob", help=f"Glob for controllers (default from config or '{DEFAULTS['controllers_glob']}').")
    args = ap.parse_args()

    repo = find_repo()
    if not repo:
        print("Not inside a git repository. Run from a project checkout.", file=sys.stderr)
        return 2

    cfg = load_config(repo)
    values_yaml_rel = args.values_yaml or cfg["values_yaml"]
    application_yml_rel = args.application_yml or cfg["application_yml"]
    controllers_glob = args.controllers_glob or cfg["controllers_glob"]

    values_yaml = repo / values_yaml_rel
    application_yml = repo / application_yml_rel

    if not values_yaml.exists():
        print(f"values.yaml not found at {values_yaml}", file=sys.stderr)
        print(f"Set 'values_yaml' in {CONFIG_FILE} or pass --values-yaml.", file=sys.stderr)
        return 2

    props = load_placeholder_props(application_yml)
    api_prefix, mappings = load_gateway_mappings(values_yaml)

    if args.files:
        groups = {f: endpoints_in_file(f, props) for f in args.files if Path(f).exists()}
    elif args.all:
        groups = {}
        for f in sorted(repo.glob(controllers_glob)):
            eps = endpoints_in_file(f, props)
            if eps:
                groups[str(f.relative_to(repo))] = eps
    else:
        base_ref = resolve_base(repo, args.base)
        if not base_ref:
            print("Could not resolve a base git ref; use --base <ref> or --all.", file=sys.stderr)
            return 2
        print(f"Checking controllers changed vs '{base_ref}'. (Use --all to audit everything.)")
        groups = changed_endpoints(repo, base_ref, props, controllers_glob)
        if not groups:
            print("No new/changed controller endpoints found on this branch. Nothing to check.")
            return 0

    return 1 if report(groups, api_prefix, mappings, values_yaml_rel) else 0


if __name__ == "__main__":
    sys.exit(main())
