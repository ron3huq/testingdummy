"""Pack cloth adapted to native body textures; exact card and league selection."""
import ctypes as C
FIELDS=('bandage_left','bandage_right')
STYLES=('Native wrist tape','White pack bandage','Black wide pack bandage','Yellow pack bandage')
_native=None

def validate_fields(values):
    for field in FIELDS:
        if field in values and (type(values[field])is not int or not 0<=values[field]<=3):
            raise ValueError('Bandage style must be Native, White, Black wide or Yellow')

def selected_rows(rows):
    defaults={row['id']:row for row in rows if row['competition']==0}
    result=[]
    for row in rows:
        validate_fields(row)
        if any(field in row for field in FIELDS):
            base=defaults.get(row['id'],{})
            result.append((int(row['id']),row['competition'],*(row.get(field,base.get(field,0))for field in FIELDS)))
    return result

def configure_native(hook):
    global _native
    import myleague_editor_runtime as editor
    rows=editor.config()['players']
    hook.noodle_bandage_add.argtypes=[C.c_uint64,C.c_uint,C.c_uint,C.c_uint]
    hook.noodle_bandage_add.restype=C.c_uint
    hook.noodle_bandage_commit.argtypes=[]
    hook.noodle_bandage_commit.restype=None
    hook.noodle_bandage_status.argtypes=[C.c_uint]
    hook.noodle_bandage_status.restype=C.c_uint64
    for pid,competition,left,right in selected_rows(rows):
        if hook.noodle_bandage_add(pid,competition,left,right)!=1:
            raise ValueError('Native bandage profile rejected')
    hook.noodle_bandage_commit()
    _native=hook

def status():
    if _native is None:
        return {'ready':False}
    labels=('ready','profiles','detail_calls','common_calls','key_applies','path_applies','last_card')
    return {name:int(_native.noodle_bandage_status(i))for i,name in enumerate(labels)}

HOOKS=(
    (0x39ca65c,bytes.fromhex('e80f19fcfd7b01a9fc6f02a9fa6703a9'),'noodle_bandage_detail_hook','configure_bandage_detail'),
    (0x392121c,bytes.fromhex('ffc302d1fd7b05a9fc6f06a9fa6707a9'),'noodle_bandage_hash_hook','configure_bandage_hash'),
    (0x39cfa14,bytes.fromhex('ff8304d1fd7b0da9fc7300f9f85f0fa9'),'noodle_bandage_common_hook','configure_bandage_common'),
)
