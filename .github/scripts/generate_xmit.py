
import os
import sys
from pathlib import Path 
from xmi import create_xmi
import shutil
import posixpath

# We ZIGI.INSTALL.PDS (as an XMIT)

execs = Path('ZIGI.EXEC')
panels = Path('ZIGI.PANELS')
samples = Path('ZIGI.SAMPLES')
lic = Path('ZIGI.GPLLIC')
readme = Path('ZIGI.README')
release = Path('ZIGI.RELEASE')
install = Path('.github/zigidata/$INSTALL')

outputfile = Path('ZIGI.INSTALL.PDS')

tmppds = Path(sys.argv[1])

shutil.copy(lic, posixpath.join(tmppds,"/GPLLIC"))
shutil.copy(readme, posixpath.join(tmppds,"/$README"))
shutil.copy(release, posixpath.join(tmppds,"/RELEASE"))
shutil.copy(install, posixpath.join(tmppds,"/$INSTALL"))

create_xmi(execs, output_file=tmppds + "/EXEC")
create_xmi(panels, output_file=tmppds + "/PANELS")
create_xmi(samples, output_file=tmppds + "/SAMPLES")
create_xmi(tmppds, output_file=outputfile)