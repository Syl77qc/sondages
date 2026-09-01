#!/usr/bin/env python3
"""Pipeline complet : un PDF déposé dans Data/ → classeur + page à jour.

    python3 .work/pipeline.py --dossier .

Détecte les sondages non encore intégrés, les extrait, les saisit, recalcule,
passe les contrôles et met la page à jour. S'arrête bruyamment au moindre doute :
mieux vaut ne rien faire que produire une projection fausse.
"""
import argparse, glob, io, os, re, subprocess, sys, shutil, tempfile
from datetime import date

PARTIS = ['CAQ','PLQ','QS','PQ','PCQ','Autre']
REGIONS_MODELE = ['Montréal RMR','Île de Montréal','Banlieue de Montréal','Québec RMR','Reste du Québec']

def normaliser(s):
    """Ramène « Léger », « leger », « Leger » à une même clé. Le classeur contient
    historiquement plusieurs graphies : on compare sur une forme canonique."""
    import unicodedata
    s = unicodedata.normalize('NFD', str(s or '')).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z]', '', s)

class Arret(Exception):
    """Condition d'arrêt : on remonte le cas plutôt que de deviner."""

# ─────────────────────────── extraction des PDF ───────────────────────────

def nombres(ligne):
    return [float(x.replace(',', '.')) for x in re.findall(r'(\d+(?:[.,]\d+)?)%', ligne)]

MOTIFS = {
    'PQ':    r'(?:Le )?Parti [Qq]uéb[ée]cois|^PQ,',
    'PLQ':   r'(?:Le )?Parti lib[ée]ral|^PLQ,',
    'CAQ':   r'(?:La )?Coalition [Aa]venir|^CAQ,',
    'PCQ':   r'(?:Le )?Parti conservateur|^(?:PCQ|Conservateur),',
    'QS':    r'Qu[ée]bec solidaire|^QS,',
    'Autre': r'Un autre parti|^Autre Parti',
}
# Léger publie une colonne « décidés » qui somme déjà à 100. Synopsis et Pallas
# publient les indécis sur une ligne distincte : leurs partis somment à ~84, et
# c'est normal. On capte donc les indécis pour valider partis + indécis ≈ 100.
MOTIF_INDECIS = r'^Ind[ée]cis'

COLONNES = {
    # firme : (indices des colonnes, dans l'ordre où elles apparaissent)
    'leger':    dict(n=r'n absolu=', prov=1, reg={'Montréal RMR':9, 'Québec RMR':10, 'Reste du Québec':11}, mini=13),
    'synopsis': dict(n=r'^\s*n=', prov=0, reg={'Île de Montréal':8, 'Banlieue de Montréal':9,
                                  'Québec RMR':10, 'Reste du Québec':11}, mini=13),
    'pallas':   dict(n=r'^Fr[ée]quence non', prov=0, reg={'Montréal RMR':7, 'Île de Montréal':8, 'Banlieue de Montréal':9,
                                  'Québec RMR':10, 'Reste du Québec':11}, mini=14),
}

def extraire(pdf, firme):
    if firme not in COLONNES:
        raise Arret(f"firme inconnue : « {firme} ». Les formats reconnus sont "
                    f"{', '.join(COLONNES)}. Un nouveau format doit être ajouté à la main "
                    f"après vérification visuelle du rapport.")
    txt = subprocess.run(['pdftotext', '-layout', pdf, '-'],
                         capture_output=True, text=True, timeout=120).stdout
    if re.search(r'grandes tendances r[ée]gionales|a cumul[ée]\s+\d+\s+sondages', txt, re.I):
        raise Arret(f"{os.path.basename(pdf)} est un rapport CUMULATIF (plusieurs sondages agrégés). "
                    f"Ses tableaux régionaux sont des graphiques, pas du texte : l'identité des partis "
                    f"s'y lit aux couleurs. Il sert aux décalages régionaux, pas au niveau national, "
                    f"et doit être saisi à la main après vérification visuelle.")
    if not txt.strip():
        raise Arret(f"{os.path.basename(pdf)} : aucun texte extrait. PDF scanné, ou tableaux "
                    f"sous forme d'images — dans ce cas l'identité des partis se lit aux couleurs "
                    f"et l'erreur serait silencieuse. Traitement manuel obligatoire.")
    spec = COLONNES[firme]
    brut = {}
    for parti, motif in MOTIFS.items():
        for ligne in txt.split('\n'):
            if re.search(motif, ligne.strip(), re.I):
                v = nombres(ligne)
                if len(v) >= spec['mini']:
                    brut[parti] = v
                    break
    indecis = None
    for ligne in txt.split('\n'):
        if re.search(MOTIF_INDECIS, ligne.strip(), re.I):
            v = nombres(ligne)
            if len(v) >= spec['mini']:
                indecis = v
                break
    manquants = [p for p in PARTIS if p not in brut]
    if manquants:
        raise Arret(f"{os.path.basename(pdf)} : partis introuvables dans le tableau — {manquants}. "
                    f"Le rapport a probablement changé de mise en page.")
    # Chaque firme annonce la taille d'échantillon différemment, et les milliers
    # sont séparés par une espace : « 1 008 » se lit comme deux nombres si on n'y
    # prend pas garde. On découpe donc sur les espaces multiples.
    n_prov = None
    lignes = txt.split('\n')
    for i, ligne in enumerate(lignes):
        if re.search(spec['n'], ligne.strip() if spec['n'].startswith('^') else ligne, re.I):
            reste = re.sub(spec['n'].lstrip('^').replace('\\s*', ''), '', ligne, count=1, flags=re.I)
            if not re.search(r'\d', reste) and i + 1 < len(lignes):
                reste = lignes[i + 1]          # Pallas met les valeurs sur la ligne suivante
            cases = [c for c in re.split(r'\s{2,}', reste.strip()) if re.search(r'\d', c)]
            if cases:
                n_prov = int(re.sub(r'\D', '', cases[spec['prov']] if len(cases) > spec['prov'] else cases[0]))
                break

    out = {}
    for nom, idx in [('PROVINCE', spec['prov'])] + list(spec['reg'].items()):
        v = [brut[p][idx] for p in PARTIS]
        total = sum(v) + (indecis[idx] if indecis else 0)
        if not (96 <= total <= 104):
            quoi = "partis + indécis" if indecis else "parts"
            raise Arret(f"{os.path.basename(pdf)} / {nom} : {quoi} somment à {total:.0f}, "
                        f"pas à 100. Colonne mal lue — la mise en page du rapport a peut-être changé.")
        s = sum(v)
        out[nom] = [x * 100 / s for x in v]   # répartition proportionnelle des indécis
    return out, n_prov

# ─────────────────────────── saisie dans le classeur ───────────────────────────

def deja_present(ws, cle):
    for r in range(4, ws.max_row + 1):
        if ws.cell(r, 1).value and f"{ws.cell(r,1).value}|{normaliser(ws.cell(r,2).value)}" == cle:
            return True
    return False

def saisir(classeur, sortie, nouveaux):
    import openpyxl
    from openpyxl.styles import Font, PatternFill
    wb = openpyxl.load_workbook(classeur)
    ws = wb['Sondages']
    bleu = Font(color='0000CC')
    ligne = ws.max_row + 1
    ajouts = 0
    for date_s, firme, n, parts in nouveaux:
        if deja_present(ws, f"{date_s}|{normaliser(firme)}"):
            print(f"  · {date_s} {firme} : déjà présent, ignoré")
            continue
        for region, v in parts.items():
            ws.cell(ligne, 1, date_s); ws.cell(ligne, 2, firme); ws.cell(ligne, 3, region)
            ws.cell(ligne, 4, n if region == 'PROVINCE' else max(n // 4, 150))
            for i in range(6):
                c = ws.cell(ligne, 5 + i, round(v[i], 1)); c.font = bleu
            modele = 4  # on recopie les formules d'une ligne existante
            for col in (11, 12, 13, 14, 15, 16, 17, 18, 19, 20):
                f = ws.cell(modele, col).value
                if isinstance(f, str) and f.startswith('='):
                    ws.cell(ligne, col, re.sub(r'(?<![A-Z$])(\d+)(?![\d:])',
                            lambda m: str(ligne) if m.group(1) == str(modele) else m.group(1), f))
            ligne += 1; ajouts += 1
    if not ajouts:
        return None
    wb.save(sortie)
    return ajouts

# ─────────────────────────── contrôles ───────────────────────────

def recalculer(chemin):
    if not shutil.which('soffice'):
        raise Arret("LibreOffice absent : impossible de recalculer le classeur.")
    d = tempfile.mkdtemp()
    subprocess.run(['soffice', '--headless', '--convert-to', 'xlsx', '--outdir', d, chemin],
                   capture_output=True, timeout=300)
    out = os.path.join(d, os.path.basename(chemin))
    if not os.path.exists(out):
        raise Arret("le recalcul par LibreOffice a échoué.")
    return out

def controles(calcule, precedent=None):
    import openpyxl, numpy as np, collections
    wb = openpyxl.load_workbook(calcule, data_only=True)
    md, sg = wb['Modèle'], wb['Sièges']
    V = np.array([[md.cell(r, 4 + k).value or 0 for k in range(6)] for r in range(2, 129)], float)
    reg = dict(collections.Counter(md.cell(r, 2).value for r in range(2, 129)))
    ech = []
    if len(V) != 127: ech.append(f"127 circonscriptions attendues, {len(V)} trouvées")
    if reg != {'Île de Montréal': 28, 'Banlieue de Montréal': 40,
               'Québec RMR': 13, 'Reste du Québec': 46}: ech.append(f"répartition régionale : {reg}")
    sieges = {}
    for r in range(6, 20):
        nom = sg.cell(r, 1).value
        if not nom or not str(nom).startswith('Scén'): continue
        v = [sg.cell(r, c).value for c in range(2, 8)]
        if any(x is None for x in v): continue
        if sum(v) != 127: ech.append(f"{nom} : {sum(v)} sièges au lieu de 127")
        sieges[re.sub(r'^Scén\.\s*', '', str(nom))] = dict(zip(PARTIS, [int(x) for x in v]))
    if abs(V.sum() - 4112821) > 200: ech.append(f"base de référence : {V.sum():,.0f} au lieu de 4 112 821")
    prov = V.sum(0) / V.sum() * 100
    if abs(prov[3] - 14.6) > 0.2 or prov[5] < 1.3:
        ech.append(f"référence provinciale suspecte : PQ {prov[3]:.2f}, Autre {prov[5]:.2f} "
                   f"(fuite « Autre → PQ » ?)")
    maxi = max(max(v.values()) for v in sieges.values()) if sieges else 0
    if maxi >= 64:
        ech.append(f"UN PARTI ATTEINT LA MAJORITÉ ({maxi}). La page affirme partout le contraire : "
                   f"elle doit être réécrite, pas rafraîchie.")
    if precedent:
        for p in PARTIS[:5]:
            d = sieges.get('A – Swing proportionnel', {}).get(p, 0) - precedent.get(p, 0)
            if abs(d) > 10:
                ech.append(f"{p} bouge de {d:+d} sièges — au-delà du seuil de 10, on s'arrête.")
    return sieges, ech

# ─────────────────────────── orchestration ───────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dossier', default='.')
    ap.add_argument('--classeur', help='par défaut : le ModeleVivantQC127 le plus récent')
    ap.add_argument('--simulation', action='store_true', help='tout vérifier sans rien écrire')
    a = ap.parse_args()
    os.chdir(a.dossier)

    classeur = a.classeur or sorted(glob.glob('ModeleVivantQC127_v*.xlsx'))[-1]
    print(f"Classeur      : {classeur}")

    import openpyxl
    ws = openpyxl.load_workbook(classeur)['Sondages']
    connus = {f"{ws.cell(r,1).value}|{normaliser(ws.cell(r,2).value)}"
              for r in range(4, ws.max_row + 1) if ws.cell(r, 1).value}

    nouveaux, ignores = [], []
    for pdf in sorted(glob.glob('Data/*.pdf')):
        m = re.match(r'(\d{4}-\d{2}-\d{2})-([a-z]+)\.pdf$', os.path.basename(pdf))
        if not m:
            print(f"  ! {os.path.basename(pdf)} : nom non conforme (AAAA-MM-JJ-firme.pdf), ignoré")
            continue
        d, firme = m.groups()
        etiquette = {'leger': 'Léger', 'synopsis': 'Synopsis', 'pallas': 'Pallas'}.get(firme, firme)
        if f"{d}|{normaliser(etiquette)}" in connus:
            continue
        try:
            parts, n = extraire(pdf, firme)
        except Arret as e:
            if 'CUMULATIF' in str(e):
                print(f"  ~ {os.path.basename(pdf)} : rapport cumulatif, ignoré (saisie manuelle)")
                ignores.append(os.path.basename(pdf))
                continue
            raise
        if not n:
            raise Arret(f"{os.path.basename(pdf)} : taille d'échantillon introuvable.")
        print(f"  → nouveau : {d} {etiquette} (n={n})")
        nouveaux.append((d, etiquette, n, parts))

    if not nouveaux:
        print("\nAucun sondage nouveau. Rien à faire.")
        return 0

    print(f"\n{len(nouveaux)} sondage(s) à intégrer.")
    for d, f, n, parts in nouveaux:
        print(f"  {d} {f} (n={n})")
        for r, v in parts.items():
            print(f"    {r:24s} " + "  ".join(f"{p} {x:4.1f}" for p, x in zip(PARTIS[:5], v)))

    if a.simulation:
        print("\n[simulation] rien n'a été écrit.")
        return 0

    n_ver = int(re.search(r'_v(\d+)', classeur).group(1))
    sortie = re.sub(r'_v\d+[^.]*', f'_v{n_ver}_{nouveaux[-1][0].replace("-","")}', classeur)
    if not saisir(classeur, sortie, nouveaux):
        print("Rien de neuf après vérification.")
        return 0
    print(f"\nClasseur écrit : {sortie}")

    calcule = recalculer(sortie)
    sieges, echecs = controles(calcule)
    print("\nSièges :")
    for k, v in sieges.items():
        print(f"  {k:42s} " + "  ".join(f"{p} {v[p]:3d}" for p in ['PQ','PLQ','CAQ','PCQ','QS']))

    if echecs:
        print("\n╔═══ ARRÊT ═══")
        for e in echecs: print("║ ✘ " + e)
        print("╚═ La page n'a PAS été mise à jour. Reprendre à la main.")
        return 2

    print("\nContrôles : tous passés ✔")
    r = subprocess.run([sys.executable, '.work/maj_artefact.py', '--classeur', sortie, '--recalculer'],
                       capture_output=True, text=True)
    print(r.stdout or r.stderr)
    print("\nIl reste UNE chose à faire à la main : relire le texte de la page,")
    print("et republier l'artefact depuis une session Claude.")
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except Arret as e:
        print(f"\n╔═══ ARRÊT ═══\n║ {e}\n╚═ Rien n'a été modifié.")
        sys.exit(2)
