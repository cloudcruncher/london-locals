"""Usage: python3 scripts/rename_brand.py "Doorstep Club" [https://newdomain.co.uk]
Renames the working name 'Locals' in templates, page builder and config, optionally sets SITE_URL, then rebuilds.
Afterwards regenerate site/img/og.png (it has the old name) and update the GitHub Pages custom domain."""
import pathlib, re, subprocess, sys
R = pathlib.Path(__file__).resolve().parent.parent
new = sys.argv[1]
files = [R/"scripts/build_pages.py", R/"scripts/templates/_head.html", R/"scripts/templates/_foot.html", R/"site/js/main.js", R/"site/config.js"]
for f in files:
    s = f.read_text()
    s = re.sub(r"\bLocals\b(?!Model)", new, s)
    if len(sys.argv) > 2 and f.name == "config.js":
        s = re.sub(r'SITE_URL:\s*"[^"]*"', f'SITE_URL: "{sys.argv[2].rstrip("/")}"', s)
    f.write_text(s)
subprocess.run([sys.executable, str(R/"scripts/build_pages.py")], check=True)
print("renamed to", new)
