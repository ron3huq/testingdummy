"""Reproduce v20 omitted stack arguments at actual UE4 instruction addresses.

This executes the original prologue, all caller-stack loads and the FString
pointer dereference. Unrelated builder logic is skipped; this is NOT a phone
or complete Game Plan integration test. The old binary must fail this test.
"""
from pathlib import Path
import json, struct, hashlib, tempfile, zipfile
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM64, UC_MODE_ARM, UC_HOOK_CODE, UcError
from unicorn.arm64_const import *

r = Path(__file__).resolve().parent
engine = Path('/workspace/ronaldo-work/apk/lib/arm64-v8a/libUE4.so')
# Addresses and stack slots independently recovered from original engine code.
loads = [
    (0x38832a0, UC_ARM64_REG_X21, 0, 1),
    (0x3883294, UC_ARM64_REG_X23, 1, 8),
    (0x3883530, UC_ARM64_REG_X28, 2, 1),
    (0x3883528, UC_ARM64_REG_X27, 3, 1),
    (0x3883524, UC_ARM64_REG_X26, 4, 1),
    (0x3883520, UC_ARM64_REG_X25, 5, 1),
    (0x388351c, UC_ARM64_REG_X24, 6, 1),
    (0x3883518, UC_ARM64_REG_X21, 7, 1),
    (0x38835e4, UC_ARM64_REG_X24, 8, 8),
    (0x3883610, UC_ARM64_REG_X26, 9, 8),
    (0x388365c, UC_ARM64_REG_X25, 10, 1),
    (0x388366c, UC_ARM64_REG_X28, 11, 1),
    (0x3883740, UC_ARM64_REG_X24, 12, 4),
    (0x3883664, UC_ARM64_REG_X27, 13, 1),
    (0x38836d8, UC_ARM64_REG_X21, 14, 8),
]

def trial(binary, enabled):
    u = Uc(UC_ARCH_ARM64, UC_MODE_ARM)
    symbols = {}
    for path, base in [(engine, 0), (binary, 0x35000000)]:
        with path.open('rb') as f:
            elf = ELFFile(f)
            for seg in elf.iter_segments():
                if seg['p_type'] != 'PT_LOAD': continue
                low = (base + seg['p_vaddr']) & ~4095
                high = (base + seg['p_vaddr'] + seg['p_memsz'] + 4095) & ~4095
                u.mem_map(low, high-low)
                u.mem_write(base+seg['p_vaddr'], seg.data())
            if base:
                symbols = {s.name: base+s['st_value'] for s in elf.get_section_by_name('.dynsym').iter_symbols()}
                for sec in elf.iter_sections():
                    if sec.name.startswith('.rela'):
                        for rel in sec.iter_relocations():
                            assert rel['r_info_type'] == 1027
                            u.mem_write(base+rel['r_offset'], struct.pack('<Q', base+rel['r_addend']))
    # Real Android ASLR does not map the ELF header at virtual address zero.
    # The harness loads engine code at link addresses, so explicitly guard NULL.
    u.mem_unmap(0, 4096)
    u.mem_map(0x30000000, 0x100000)
    stop, stack, out = 0x30000000, 0x300f0000, 0x30002000
    values = [0x30004000 + i*0x100 + i for i in range(15)]
    for slot in [0,2,3,4,5,6,7,10,11,13]: values[slot] = (slot+1)%2
    values[12] = 93
    # Valid FString-like object consumed at 0x3883628: arg16, not forwarded by v20.
    u.mem_write(values[8], struct.pack('<Qii', 0x30009000, 19, 20))
    state = {'phase': None, 'seen': [], 'dereference': None}
    def boundary(uc, pc, size, data):
        if state['phase'] is None: return
        if pc == 0x3883268:  # real prologue completed, FP=original SP-0x60
            state['phase'] = 0
            uc.reg_write(UC_ARM64_REG_PC, loads[0][0]); return
        index = state['phase']
        if isinstance(index, int) and index < len(loads) and pc == loads[index][0]+4:
            address, reg, slot, width = loads[index]
            actual = uc.reg_read(reg)
            expected = values[slot] & ((1 << (width*8))-1)
            state['seen'].append({'pc': hex(address), 'argument': slot+8, 'actual': actual, 'expected': expected})
            # Continue even on mismatch to exercise the real bad pointer dereference.
            state['phase'] = index+1
            if index+1 < len(loads): uc.reg_write(UC_ARM64_REG_PC, loads[index+1][0])
            else: uc.reg_write(UC_ARM64_REG_PC, 0x38835e4)
            return
        if index == len(loads) and pc == 0x38835e8:
            state['phase'] = 'pointer'
            uc.reg_write(UC_ARM64_REG_PC, 0x3883628); return
        if index == 'pointer' and pc == 0x388362c:
            state['dereference'] = uc.reg_read(UC_ARM64_REG_X22)
            state['phase'] = 'epilogue'
            uc.reg_write(UC_ARM64_REG_PC, 0x38837ec)  # original callee-save restore/RET
    u.hook_add(UC_HOOK_CODE, boundary)
    def call(address, *args):
        u.reg_write(UC_ARM64_REG_SP, stack)
        u.reg_write(UC_ARM64_REG_LR, stop)
        for i, v in enumerate(args[:8]): u.reg_write(UC_ARM64_REG_X0+i, v)
        if len(args)>8: u.mem_write(stack, struct.pack('<'+'Q'*(len(args)-8), *args[8:]))
        u.emu_start(address, stop, count=100000)
    call(symbols['configure_card_data_ext'], 0, 0x3883248)
    call(symbols['noodle_enable'], enabled)
    state['phase'] = 'prologue'
    fault = None
    try: call(symbols['noodle_card_data_ext_hook'], out, 1, 2, 3, 4, 5, 6, 7, *values)
    except UcError as exc: fault = str(exc)
    passed = not fault and len(state['seen']) == 15 and all(x['actual']==x['expected'] for x in state['seen']) and state['dereference']==19
    return {'passed': passed, 'enabled': enabled, 'fault': fault, **state}

if __name__ == '__main__':
    old = r.parents[1]/'player-faces-v20/source/libnoodle_hair.so'
    baseline_tmp = tempfile.TemporaryDirectory(prefix='v20-original-binary-')
    if not old.exists():
        old = Path(baseline_tmp.name)/'libnoodle_hair.so'
        with zipfile.ZipFile(r.parents[1]/'player-faces-v20/Faces-v20-14-cards-4-teams.zip') as z:
            old.write_bytes(z.read('work/tools/libnoodle_hair.so'))
    assert hashlib.sha256(old.read_bytes()).hexdigest() == '320144792669845ee852707011b5462d5d2bb41cedbc74d54cf93739bc55fdd3'
    results = {'v20_before': trial(old, 0), 'v20a_disabled': trial(r/'libnoodle_hair.so', 0), 'v20a_enabled': trial(r/'libnoodle_hair.so', 1)}
    assert not results['v20_before']['passed']
    assert results['v20_before']['fault'] and 'READ_UNMAPPED' in results['v20_before']['fault']
    assert results['v20a_disabled']['passed'] and results['v20a_enabled']['passed']
    results.update(status='OLD_CRASH_REPRODUCED_NEW_23_ARGUMENTS_PASS', phone_tested=False, boundary='Original prologue/15 stack loads/FString pointer load/epilogue execute; unrelated native builder body skipped.')
    (r.parent/'squad-abi-validation.json').write_text(json.dumps(results, indent=2))
    print(results['status'])
