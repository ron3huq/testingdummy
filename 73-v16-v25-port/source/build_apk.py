"""Build/sign the V25 test from the exact user's 73 V16 APK. Never installs or deletes app data."""
import hashlib,json,os,pathlib,shutil,subprocess,sys,zipfile
# APK ZIP offsets are unsigned 32-bit; Python's conservative 2 GiB
# ZIP64 threshold would produce an APK rejected by Android signing tools.
zipfile.ZIP64_LIMIT=(1<<32)-1
ROOT=pathlib.Path(__file__).resolve().parent
EXPECTED='04f3e86e129bc7ef1705120caa93e43284f2033fffc376c4d597e5c7ddc15499'
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def main():
 args=[x for x in sys.argv[1:] if x!='--unsigned-only']
 unsigned_only='--unsigned-only' in sys.argv
 source=pathlib.Path(args[0]).resolve() if args else ROOT/'73efootball-V16.apk'
 if not source.is_file():raise RuntimeError('Place original 73efootball-V16.apk beside this script, or pass its path.')
 print('Checking original APK...',flush=True)
 if sha(source)!=EXPECTED:raise RuntimeError('Wrong APK. Requires the exact 73 V16 uploaded to releasee; input untouched.')
 java=shutil.which('java')
 if not java:raise RuntimeError('Install Java 17 or newer, then run again.')
 signer=ROOT/'uber-apk-signer-1.3.0.jar'
 if sha(signer)!='e1299fd6fcf4da527dd53735b56127e8ea922a321128123b9c32d619bba1d835':raise RuntimeError('Signer checksum mismatch')
 out=ROOT/'output';out.mkdir(exist_ok=True);apk=out/'73-V16-V25-unsigned.apk'
 if source==apk:raise RuntimeError('Input must be original APK')
 if apk.exists():raise RuntimeError('output already contains unsigned APK; move old output away before rebuilding')
 if shutil.disk_usage(out).free<source.stat().st_size*(1 if unsigned_only else 3)+500_000_000:raise RuntimeError('Need about 8 GB free disk space to build and sign.')
 files={p.relative_to(ROOT/'payload').as_posix():p for p in (ROOT/'payload').rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
 manifest=json.loads((ROOT/'release-manifest-v25.json').read_text(encoding='utf-8'))
 listed={x['path']:x for x in manifest['files']}
 for n,p in files.items():
  row=listed[n]
  if p.stat().st_size!=row['bytes'] or sha(p)!=row['sha256']:raise RuntimeError('Payload mismatch: '+n)
 print('Creating separate test APK; original stays unchanged...',flush=True);shutil.copyfile(source,apk)
 replacements={'assets/chaquopy/app.imy':ROOT/'app-v25.imy','assets/gateway-release/release-manifest.json':ROOT/'release-manifest-v25.json'}
 replacements.update({'assets/gateway-release/'+n:p for n,p in files.items()})
 with zipfile.ZipFile(apk,'a',allowZip64=True) as z:
  # Keep original local offsets (including engine library alignment), remove old
  # signature entries and replaced names from the central directory only.
  z.filelist=[i for i in z.filelist if i.filename not in replacements and not i.filename.upper().startswith('META-INF/')]
  z.NameToInfo={i.filename:i for i in z.filelist}
  for n,p in replacements.items():z.write(p,n,compress_type=zipfile.ZIP_STORED)
 with zipfile.ZipFile(apk) as z:
  assert len(z.namelist())==len(set(z.namelist()))
  for n,p in replacements.items():
   with z.open(n) as f:
    h=hashlib.sha256()
    for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
   assert h.hexdigest()==sha(p),n
 if unsigned_only:
  print('Unsigned test assembly complete: '+str(apk));return
 print('Aligning, signing and verifying APK...',flush=True)
 subprocess.run([java,'-Xmx512m','-jar',str(signer),'-a',str(apk),'-o',str(out),'--allowResign'],check=True,cwd=ROOT)
 signed=list(out.glob('*aligned-debugSigned.apk'))
 if len(signed)!=1:raise RuntimeError('Could not identify signed APK; inspect signer output')
 result=signed[0];(out/'SHA256SUMS.txt').write_text(sha(result)+'  '+result.name+'\n',encoding='ascii')
 print('\nDONE: '+str(result)+'\nThis is a test build; back up/export saves before replacing the original app. No installation was performed.',flush=True)
if __name__=='__main__':
 try:main()
 except Exception as e:print('ERROR: '+str(e));sys.exit(1)
