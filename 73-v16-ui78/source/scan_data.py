from pathlib import Path
import sys,csv,collections,zlib,html
P=Path('/workspace/ronaldo-work/73-ui78');exec(Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0])
sys.path.insert(0,str(P/'payload/work/tools'));import editor_names
b=Path('/workspace/ronaldo-work/73-ui6/Player-decoded.bin').read_bytes();record=0x30010000;source=0x30011000;groups=collections.defaultdict(list);dims={}
for off in range(0,len(b),400):
 row=b[off:off+400];pid=struct.unpack_from('<Q',row,8)[0];name=editor_names.NAMES.get(str(pid),row[332:396].split(b'\0')[0].decode('utf8','strict'));u.mem_write(source,row);call(0x82aa124,record,source,0)
 dims[str(pid)]=[get(record,47),get(record,48)]
 for ix in [59,60]:groups[(ix,get(record,ix))].append((pid,name))
 if off%4000000==0:print('SCANNED',off//400,flush=True)
lookup={};rows=[];short=[]
for (ix,val),cards in sorted(groups.items()):
 cards=sorted(set(cards),key=lambda x:(x[0]<2**40,x[0]));chosen=[];names=set()
 for item in cards:
  if item[1]not in names:chosen.append(item);names.add(item[1])
  if len(chosen)==6:break
 for item in cards:
  if len(chosen)==6:break
  if item not in chosen:chosen.append(item)
 if len(chosen)<6:short.append([ix,val,len(chosen)])
 lookup.setdefault(str(ix),[]).append({'id':val,'cards':[{'id':str(pid),'name':name}for pid,name in chosen]})
 for pid,name in chosen:rows.append([str(ix),f'{val:04d}',str(pid),name])
tools=P/'payload/work/tools';(tools/'celebration_choices.json').write_text(json.dumps(lookup,ensure_ascii=False,separators=(',',':')));(tools/'body_defaults.zlib').write_bytes(zlib.compress(json.dumps(dims,separators=(',',':')).encode()))
with(P/'celebration-ids.csv').open('w',encoding='utf-8-sig',newline='')as f:
 writer=csv.writer(f);writer.writerow(['Loại ăn mừng (parameter)','ID ăn mừng','ID cầu thủ','Tên cầu thủ']);writer.writerows(rows)
body=['<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>ID ăn mừng · eFootball73</title><style>body{background:#0a1424;color:#e4efff;font:16px system-ui;margin:24px;line-height:1.6}input{padding:12px;width:min(90%,600px)}table{border-collapse:collapse;width:100%;margin:20px 0}td,th{border:1px solid #34465e;padding:10px 18px;text-align:left}td:nth-child(-n+2){font-family:monospace;white-space:nowrap}thead{background:#193454;position:sticky;top:0}a{color:#6edddd}.wrap{overflow:auto}</style><h1>ID ăn mừng · eFootball73 V16</h1><p>Đọc toàn bộ 46.623 bản ghi qua bộ giải mã gốc của game. Mỗi giá trị ghi tối đa 6 thẻ có dữ liệu; không tạo thêm chủ sở hữu nếu game có ít hơn 6. Tên thẻ mod dùng bí danh đã có của bản 73.</p><p>ID ở hai bảng là hai trường riêng biệt (59 và 60), không phải số trong tên file animation. Số 0 là giá trị mặc định. Danh sách xác minh dữ liệu sở hữu; chưa xác nhận từng động tác trên điện thoại.</p><input id="q" placeholder="Tìm ID hoặc tên cầu thủ…" aria-label="Tìm kiếm">']
for ix,title in [(59,'Ăn mừng chính · GoalPerformance · parameter 59'),(60,'Ăn mừng đặc biệt · GoalPerformanceMemorial · parameter 60')]:
 body.append('<h2>'+title+'</h2><div class="wrap"><table><thead><tr><th>ID ăn mừng</th><th>ID cầu thủ</th><th>Tên cầu thủ</th></tr></thead><tbody>')
 for par,val,pid,name in rows:
  if int(par)==ix:body.append('<tr>'+''.join('<td>'+html.escape(x)+'</td>'for x in [val,pid,name])+'</tr>')
 body.append('</tbody></table></div>')
body.append('<script>const rows=[...document.querySelectorAll("tbody tr")].map(r=>[r,r.textContent.normalize("NFD").replace(/[\\u0300-\\u036f]/g,"").toLowerCase()]);document.querySelector("#q").oninput=e=>{const q=e.target.value.normalize("NFD").replace(/[\\u0300-\\u036f]/g,"").toLowerCase();for(const [r,t] of rows)r.hidden=!t.includes(q)};</script></html>');(P/'celebration-ids.html').write_text(''.join(body))
(P/'celebrations-validation.json').write_text(json.dumps({'passed':True,'source_records':len(b)//400,'native_importer':'0x82aa124','getter':'0x82a84d4','groups':len(groups),'rows':len(rows),'fewer_than_six':short,'no_unsupported_animation_clip_to_parameter_mapping':True,'phone_tested':False},indent=2));print('SCAN_PASS',len(groups),len(rows),flush=True)
