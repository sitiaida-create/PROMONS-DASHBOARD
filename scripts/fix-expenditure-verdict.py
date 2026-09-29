from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")

old = """  // Geran yang berstatus Cemerlang atau Baik telah disahkan mencapai kesemua KPI >= 100%
  const v = String(verdict || "").toUpperCase().trim();
  if (v.includes("CEMERLANG") || v.includes("EXCELLENT") || v.includes("BAIK") || v.includes("GOOD")) {
    return false;
  }
"""

new = """  // New Verdict tidak boleh override nilai KPI sebenar untuk Geran Tamat.
  // Khususnya, Expenditure <100% mesti dikira walaupun verdict = Baik/Cemerlang.
  const v = String(verdict || "").toUpperCase().trim();
  if (!(currentSource === "Geran Tamat" && itemType === "EXPENDITURE")) {
    if (v.includes("CEMERLANG") || v.includes("EXCELLENT") || v.includes("BAIK") || v.includes("GOOD")) {
      return false;
    }
  }
"""

if old not in text:
    raise SystemExit("Patch berhenti: blok sasaran tidak ditemui; index.html tidak diubah.")

if text.count(old) != 1:
    raise SystemExit(f"Patch berhenti: blok sasaran ditemui {text.count(old)} kali; index.html tidak diubah.")

path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("Patch berjaya diterapkan.")
