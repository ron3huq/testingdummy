def configuration():
    try:
        data=json.loads((HERE/'noodle_hair.json').read_text())
        return data.get('enabled') is True
    except Exception:
        return False


def bundle():
    meta=json.loads((HERE/'noodle_bundle.json').read_text())
    if meta.get('target_card_id')!='88044950524330' or meta.get('container')!='pc9298_mobile_and':
        raise ValueError('unexpected noodle bundle identity')
    root=HERE.parent.parent/'livedata'
    for ext in ['pak','utoc','ucas']:
        name='pc9298_mobile_and.'+ext;path=root/name;item=meta['files'][name]
        if path.stat().st_size!=item['size'] or digest(path)!=item['sha256']:
            raise ValueError('noodle asset checksum mismatch: '+name)
    if digest(HERE/'libnoodle_hair.so')!=HOOK_SHA:
        raise ValueError('noodle native module checksum mismatch')
    return meta


def advertise(value,port):
    """Copy only CMD_LOGIN_LIVEDATA-shaped objects; preserve the rest of login."""
    global _advertised
    if not isinstance(value,dict) or not isinstance(value.get('version_file'),str) or not isinstance(value.get('livedata_list'),list):
        return value
    # Keep the mounted bundle/version stable when only visual redirection is disabled.
    try:
        meta=bundle();version=json.loads(value['version_file'])
        if not isinstance(version.get('dt880'),list) or type(version.get('version')) is not int:
            raise ValueError('unrecognized live-data version schema')
        if type(port) is not int or not 1<=port<=65535:
            raise ValueError('invalid gateway listener')
        stem='pc9298_mobile_and';rows={ext:meta['files'][stem+'.'+ext] for ext in ['pak','utoc','ucas']}
        item={'name':'pc9298','hash':rows['pak']['sha256'],'hashFileSize':rows['pak']['size'],'ucas':rows['ucas']['sha256'],'ucasFileSize':rows['ucas']['size'],'utoc':rows['utoc']['sha256'],'utocFileSize':rows['utoc']['size']}
        # Idempotent if another wrapper calls us again on the already rewritten object.
        previous=next((row for row in version['dt880'] if isinstance(row,dict) and row.get('name')=='pc9298'),None)
        if previous!=item:
            version['version']+=19
            if version['version']>=2**31:raise ValueError('live-data version overflow')
        version['dt880']=[row for row in version['dt880'] if not isinstance(row,dict) or row.get('name')!='pc9298']+[item]
        result=dict(value);result['version_file']=json.dumps(version,separators=(',',':'))
        names={stem+'.'+ext for ext in ['pak','utoc','ucas']}
        result['livedata_list']=[row for row in value['livedata_list'] if not isinstance(row,dict) or row.get('name') not in names]
        result['livedata_list'] += [{'name':stem+'.'+ext,'size':rows[ext]['size'],'url':'http://127.0.0.1:'+str(port)+'/livedata/'+stem+'.'+ext} for ext in ['pak','utoc','ucas']]
        _advertised+=1
        return result
    except Exception as exc:
        try:(HERE/'noodle-advertise-error.txt').write_text(str(exc))
        except Exception:pass
        return value


def report():
    fields=['load_calls','target_calls','redirects','nonnull_callbacks','null_callbacks','skipped_face_id','busy_skips','disabled_calls','restore_requests','reserved','last_target_id']
    result={'state':_state,'version':'ronaldo-noodle-trial-v1','device_verified':False,'error':_error,'enabled':configuration(),'payload_verified':_payload_ok,'manifest_advertised':_advertised,'target_card_id':'88044950524330'}
    if _handle is not None:
        result.update({name:int(_handle.noodle_stat(i)) for i,name in enumerate(fields)})
        result['last_face_id']=''.join(chr(_handle.noodle_face_char(i)) for i in range(64)).split('\0',1)[0]
    try:
        path=HERE/'noodle-hair-status.json';tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(result,indent=2));tmp.replace(path)
    except Exception:pass


def worker():
    global _handle,_payload_ok,_state,_error
    try:
        bundle();_payload_ok=True
        if platform.machine().lower() not in ('aarch64','arm64') or C.sizeof(C.c_void_p)!=8:
            raise RuntimeError('only Android ARM64 supported')
        _state='WAITING_FOR_LIBUE4';report()
        for _ in range(300):
            matches=[row for row in maps() if row[4].endswith('/libUE4.so') and row[3]==0]
            if matches:
                base=matches[0][0];path=matches[0][4]
                handle=install(base,path,entry=0x39d3e1c,prologue=bytes.fromhex('ff4302d1fd7b03a9fc6f04a9fa6705a9'),hook_name='noodle_done_hook',configure_name='configure_done')
                _handle=handle
                handle.noodle_enable.argtypes=[C.c_uint32];handle.noodle_enable.restype=None
                handle.noodle_stat.argtypes=[C.c_uint32];handle.noodle_stat.restype=C.c_uint64
                handle.noodle_face_char.argtypes=[C.c_uint32];handle.noodle_face_char.restype=C.c_uint32
                install(base,path,hook_name='noodle_load_hook',configure_name='configure_load')
                _state='HOOK_ACTIVE'
                while True:
                    handle.noodle_enable(int(configuration()));report();time.sleep(1)
            time.sleep(1)
        raise RuntimeError('libUE4.so did not become available')
    except Exception as exc:
        _state='ERROR';_error=str(exc)
        if _handle is not None:
            try:_handle.noodle_enable(0)
            except Exception:pass
        report()


def start():
    global _started
    if _started:return
    _started=True;threading.Thread(target=worker,name='noodle-hair',daemon=True).start()
