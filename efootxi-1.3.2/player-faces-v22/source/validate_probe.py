"""Execute read-only native draw collection, 64-bit diagnostic reconstruction,
throttle and independent per-card snapshots. Engine query bodies are modeled.
"""
from pathlib import Path
exec((Path(__file__).resolve().parent/'validate_native_v21.py').read_text())
probe_checks=[];cache_chars=0x30280000
def key(name):
    found=next((k for k,v in names.items()if v==name),None)
    if found is None:found=len(names)+1;names[found]=name
    return found
def obj(address,name,cls=0):
    u.mem_write(address+0x18,struct.pack('<Q',key(name)))
    if cls:u.mem_write(address+0x10,struct.pack('<Q',cls))
def cname(sample,row,field):
    p=call(syms['noodle_draw_text'],sample,row,field)
    return bytes(u.mem_read(p,192)).decode('utf-16-le').split('\0')[0]
component=0x30400000;body_component=0x30401000;other_component=0x30402000
private=0x30403000;body_mesh=0x30404000;other_mesh=0x30405000;material=0x30406000
dynclass=0x30407000;parent=0x30408000;shader=0x30409000;diffuse=0x3040a000;blackrt=0x3040b000
constclass=0x3040c000;materialclass=0x3040d000;grandparent=0x3040e000;vt=0x3040f000
obj(dynclass,'MaterialInstanceDynamic');obj(constclass,'MaterialInstanceConstant');obj(materialclass,'Material')
obj(private,'SK_NT01ep00v0313_Face');obj(body_mesh,'SK_002d01');obj(other_mesh,'SK_116541_Face')
obj(material,'MaterialInstanceDynamic_Test',dynclass);obj(parent,'MI_ND06ep00v0313_Head_FaceLegacy_HQ',constclass);obj(grandparent,'MI_Head_FaceLegacy_HQ',constclass);obj(shader,'M_Head_Face_HQ',materialclass)
obj(diffuse,'T_ND06ep00v0313_Face_D');obj(blackrt,'TextureRenderTarget2D_Diagnostic')
u.mem_write(material+0xd0,struct.pack('<Q',parent));u.mem_write(parent+0xd0,struct.pack('<Q',grandparent));u.mem_write(grandparent+0xd0,struct.pack('<Q',shader))
stub=0x33018200;u.mem_write(stub,struct.pack('<I',0xd65f03c0));u.mem_write(vt+0x588,struct.pack('<Q',stub))
for c,m in [(component,private),(body_component,body_mesh),(other_component,other_mesh)]:
    u.mem_write(c,struct.pack('<Q',vt));u.mem_write(c+0x468,struct.pack('<Q',m));u.mem_write(c+0x210,struct.pack('<I',0x100c0000))
arr=0x30411000;u.mem_write(arr,struct.pack('<QQ',body_component,component));u.mem_write(actor+0x228,struct.pack('<Q',component));u.mem_write(actor+0x1a70,struct.pack('<Qii',arr,2,2));u.mem_write(actor+0x1a80,struct.pack('<Qii',arr+16,1,1));u.mem_write(arr+16,struct.pack('<Q',other_component));u.mem_write(actor+0x1ad0,struct.pack('<Qii',arr,33,33))
for off,texture in [(0x1a40,blackrt),(0x1a48,diffuse),(0x1a90,blackrt),(0x1a98,diffuse)]:u.mem_write(actor+off,struct.pack('<Q',texture))
def probe_boundary(uc,address,size,data):
    if address==0x4415ac8:
        name=names[struct.unpack('<Q',uc.mem_read(uc.reg_read(UC_ARM64_REG_X0),8))[0]]
        fstring(uc.reg_read(UC_ARM64_REG_X1),name,cache_chars);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
    elif address==stub:
        uc.reg_write(UC_ARM64_REG_X0,material);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
    elif address==0x59b8a2c:
        parameter=names[uc.reg_read(UC_ARM64_REG_X1)];uc.reg_write(UC_ARM64_REG_X0,blackrt if parameter=='faceBaseColor'else diffuse if parameter=='BaseColorMap'else 0);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,probe_boundary)
snapshot=[bytes(u.mem_read(c,0x600))for c in [component,body_component,other_component]]
call(syms['noodle_enable'],1);u.mem_write(actor+0x10b0,struct.pack('<Q',105807861630781));u.mem_write(closure,struct.pack('<Q',actor));u.mem_write(result,struct.pack('<Q',private));call(done,closure,result,detail)
sample=next(i for i in range(8)if call(syms['noodle_draw_value'],i,8,0)==(105807861630781&0xffffffff))
assert call(syms['noodle_draw_value'],sample,8,2)==3
assert cname(sample,0,0)=='SK_NT01ep00v0313_Face'and cname(sample,1,0)=='SK_002d01'and cname(sample,2,0)=='SK_116541_Face'
assert cname(sample,0,1)=='MaterialInstanceDynamic_Test'and cname(sample,0,2).startswith('MI_ND06')
assert cname(sample,0,3)=='TextureRenderTarget2D_Diagnostic'and cname(sample,0,4).startswith('T_ND06')
assert cname(sample,0,9)=='TextureRenderTarget2D_Diagnostic'and cname(sample,0,10).startswith('T_ND06')
assert cname(sample,0,7)=='MI_Head_FaceLegacy_HQ'and cname(sample,0,8)=='M_Head_Face_HQ'
assert all(bytes(u.mem_read(c,0x600))==before for c,before in zip([component,body_component,other_component],snapshot))
probe_checks.append('primary_material_texture_shader_chain_and_secondary_names_collected_without_render_writes')
generation=call(syms['noodle_draw_value'],sample,8,3)
for i in range(255):call(bake,actor)
assert call(syms['noodle_draw_value'],sample,8,3)==generation
call(bake,actor);assert call(syms['noodle_draw_value'],sample,8,3)>generation
probe_checks.append('native_probe_throttled_256_bakes')
for card in [target,89135066911146]:
    u.mem_write(actor+0x10b0,struct.pack('<Q',card));call(done,closure,result,detail)
found=[]
for i in range(8):
    if call(syms['noodle_draw_value'],i,8,3):found.append(call(syms['noodle_draw_value'],i,8,0)|(call(syms['noodle_draw_value'],i,8,1)<<32))
assert set([105807861630781,target,89135066911146])<=set(found)
probe_checks.append('per_card_samples_retained_for_test_original_and_working_control')
request(105807861630781,'116541');actual=call(syms['noodle_stat'],10);lo=call(syms['noodle_stat_word'],10,0);hi=call(syms['noodle_stat_word'],10,1)
signed_lo=lo-(1<<32)if lo&(1<<31)else lo
assert actual==105807861630781==((hi&0xffffffff)<<32)|(signed_lo&0xffffffff)
probe_checks.append('full64_ID_diagnostics_reconstructed_even_with_signed32_ctypes_returns')
with_texture=True;es=request(105807861630781,'116541');with_texture=False
assert any(e[0]=='mesh'and'SK_NT01'in e[1]for e in es)and any(e[0]=='path'and'T_ND06'in e[1]for e in es)
probe_checks.append('material_control_mesh_NT01_and_texture_ND06_paths_are_consistent')
(r.parent/'probe-validation.json').write_text(json.dumps({'status':'V22_READ_ONLY_PROBE_AND_FULL64_DIAGNOSTICS_PASS','checks':probe_checks,'query_bodies_modeled':True,'phone_tested':False},indent=2));print('V22_READ_ONLY_PROBE_AND_FULL64_DIAGNOSTICS_PASS')
