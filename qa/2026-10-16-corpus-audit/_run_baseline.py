import json,pathlib,subprocess,sys,concurrent.futures,hashlib,os,time
ROOT=pathlib.Path(r"C:/Users/Declan/Documents/Projects/Skills-and-Automation/contents-production-skills")
Q=ROOT/"qa/2026-10-16-corpus-audit"
blocks=json.loads((Q/"_blocks.json").read_text(encoding="utf-8"))
S=pathlib.Path(r"C:/Users/Declan/AppData/Local/Temp/cpsbook")
S.mkdir(parents=True,exist_ok=True)
def run(item):
    key,prompt=item
    out=S/("bl_%s.json"%key.split()[0].replace('/','_'))
    if out.exists(): return key,"cached"
    pre="\n\n[END OF PROMPT. Answer the question above directly. Do not edit any file.]\n"
    t0=time.time()
    r=subprocess.run([r"C:/Users/Declan/AppData/Roaming/npm/codex.cmd","exec","--sandbox","read-only","--skip-git-repo-check",prompt+pre],
        cwd=str(ROOT),capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=900)
    out.write_text(json.dumps({"key":key,"prompt":prompt,"stdout":r.stdout,"stderr":r.stderr[-3000:],"rc":r.returncode,"secs":round(time.time()-t0,1)},ensure_ascii=False),encoding="utf-8")
    return key,r.returncode
items=[(k,v) for k,v in blocks.items() if k!="Scoring"]
which=sys.argv[1] if len(sys.argv)>1 else "all"
allow=sys.argv[2].split(",") if len(sys.argv)>2 else None
if allow: items=[(k,v) for k,v in items if k.split()[0] in allow]
print("running",len(items))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
    for k,rc in ex.map(run,items): print(k,rc,flush=True)
