// Récolte des séries de sondages de qc125.com
// À exécuter dans la console du navigateur (ou via javascript_tool) sur CHACUNE des deux pages :
//   https://qc125.com/sondages.htm        → National, MTL, QC, REG
//   https://qc125.com/sondages-demo.htm   → m, f, age1, age2, age3, FR, NF
// Le paramètre ?demo= de l'URL ne sert à rien : tout est déjà dans l'objet ci-dessous.
// Colonnes des valeurs, dans l'ordre : CAQ | PLQ | QS | PQ | PCQ
(() => {
  const T = window.demopoll_TABLE_DATA?.demos;
  if (!T) return "demopoll_TABLE_DATA absent — page pas encore chargée ?";
  const DEPUIS = "2025-01-01";                        // ajuster au besoin
  const lignes = ["demo|date|firme|n|CAQ|PLQ|QS|PQ|PCQ"];
  for (const cle of Object.keys(T)) {
    for (const r of T[cle].rows) {
      if (r.generalelx || r.date < DEPUIS) continue;   // exclut les résultats d'élection
      const firme = r.firm.replace(/ Research| Recherche| Data| Strategies/, "");
      const n = String(r.sample).replace(/\s/g, "");
      const v = r.cells.map(c => (c.label || "").replace("*", ""));  // * = tranche recodée
      lignes.push([cle, r.date, firme, n, ...v].join("|"));
    }
  }
  return lignes.join("\n");
})();
