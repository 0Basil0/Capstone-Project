from pathlib import Path
import polib
base = Path(r"c:\Users\plati\OneDrive\Desktop\Capstone-Project")
compiled = []
for po in base.rglob('LC_MESSAGES/*.po'):
    mo = po.with_suffix('.mo')
    print('Compiling', po, '->', mo)
    p = polib.pofile(str(po))
    p.save_as_mofile(str(mo))
    compiled.append(str(mo))
print('Done. Compiled:', compiled)
