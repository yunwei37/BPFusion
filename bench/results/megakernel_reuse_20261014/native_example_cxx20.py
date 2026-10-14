import pathlib,runpy,sys,torch.utils.cpp_extension as cpp
original=cpp.load
def compatible_load(*args,**kwargs):
 flags=kwargs.get('extra_cflags')
 if flags and '-std=c++17' in flags:
  kwargs['extra_cflags']=['-std=c++20' if flag=='-std=c++17' else flag for flag in flags]
  print('COMPAT_HOST_CXX17_TO_CXX20; CUDA flags/source unchanged',flush=True)
 return original(*args,**kwargs)
cpp.load=compatible_load
r=pathlib.Path(__file__).parent
record=__import__('json').loads((r/'native_example_command.json').read_text())
sys.argv=record['command'][1:]
runpy.run_path(sys.argv[0],run_name='__main__')
