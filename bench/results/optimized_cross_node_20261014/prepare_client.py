import pathlib,json,sys
root=pathlib.Path('/tmp/bpfusion-optimized-cross-node-nk49zfoa')
model,pair,mode,stage=sys.argv[1:];pair=int(pair)
config=json.loads((root/'models.json').read_text())[model]
pool={(tuple(r['prompt']),r['gen']):{tuple(s) for s in r['sequences']} for r in config['frozen_model']['references']}
prefix=stage+'_'+model+'_p'+str(pair)+'_'+mode
matrix=[(1,1),(64,1),(1,8),(64,8)]
matrix=matrix[pair%4:]+matrix[:pair%4]
body=(root/'client.py').read_text()+'\nBASE='+repr(dict(pair=pair,mode=mode))+'\nPROMPTS='+repr(config['prompts'])+'\nPOOL='+repr(pool)+'\nMATRIX='+repr(matrix)+'\nCOUNT='+str(8 if stage=='preflight' else 64)+'\nos.environ["BF_BIND"]="10.42.1.238"\nrun()\n'
(root/(prefix+'.client.py')).write_text(body)
wrapper="import pathlib,subprocess,json; p=pathlib.Path('/tmp/"+prefix+"'); a=open(str(p)+'.client.stdout','w'); b=open(str(p)+'.client.stderr','w'); r=subprocess.run(['python3',str(p)+'.client.py'],stdout=a,stderr=b);a.close();b.close();open(str(p)+'.client_exit.json','w').write(json.dumps(dict(exit=r.returncode)))"
launch="import pathlib,subprocess,json\np=pathlib.Path('/tmp/"+prefix+"')\npathlib.Path(str(p)+'.client.py').write_text("+repr(body)+")\nr=subprocess.Popen(['python3','-c',"+repr(wrapper)+"],start_new_session=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)\npathlib.Path(str(p)+'.client_started.json').write_text(json.dumps(dict(pid=r.pid)))\nprint(json.dumps(dict(pid=r.pid,prefix=str(p))))\n"
(root/(prefix+'.client_launch.py')).write_text(launch)
print(json.dumps(dict(launch=launch)))
