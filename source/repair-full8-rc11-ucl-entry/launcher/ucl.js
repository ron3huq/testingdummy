"use strict";
(() => {
  const UI=()=>window.EditorUI.U;
  const api=payload=>UI().api("ucl",payload||{});
  const phases={LEAGUE_PHASE:"League phase",PLAYOFFS:"Play-off",R16:"Vòng 1/8",QF:"Tứ kết",SF:"Bán kết",FINAL:"Chung kết",CHAMPION:"Vô địch",ELIMINATED:"Đã kết thúc"};
  const levels={VERYEASY:"Rất dễ",EASY:"Dễ",NORMAL:"Bình thường",HARD:"Khó",VERYHARD:"Rất khó",HARDEST:"Siêu sao",LEGEND:"Huyền thoại"};
  const names=s=>new Map(s.teams.map(t=>[t.team_id,t.name||t.short||"Câu lạc bộ"]));
  const label=(map,id)=>map.get(id)||"Câu lạc bộ";
  const button=(label,value,kind)=>({label,value,kind});
  const options=(select,rows)=>rows.forEach(([value,text])=>select.append(UI().h("option",{value},text)));
  function table(headers,rows,classes){
    const h=UI().h,body=h("tbody");rows.forEach((row,i)=>body.append(h("tr",{class:classes?classes(i):""},row.map(value=>h("td",{},value)))));
    return h("div",{class:"ucl-scroll"},h("table",{class:"ucl-table"},h("thead",{},h("tr",{},headers.map(text=>h("th",{},text)))),body));
  }
  async function standings(status){
    const s=status.season,map=names(status),rows=s.ranking;
    const pane=table(["#","CLB","Trận","HS","Điểm"],rows.map(t=>[t.rank,label(map,t.team_id),t.played,t.gd,t.points]),i=>(rows[i].rank<=8?"ucl-direct":rows[i].rank<=24?"ucl-playoff":"")+(rows[i].team_id===s.own?" ucl-own":""));
    const promise=UI().sheet("Bảng xếp hạng UCL","1–8: vào thẳng vòng 1/8 · 9–24: play-off · 25–36: bị loại",[UI().ok("Quay lại")],pane);
    requestAnimationFrame(()=>{const own=pane.querySelector(".ucl-own");if(own)pane.scrollTop+=own.getBoundingClientRect().top-pane.getBoundingClientRect().top-pane.clientHeight/2+own.clientHeight/2;});
    await promise;
  }
  async function fixtures(status){
    const h=UI().h,s=status.season,map=names(status),groups=new Map();
    for(const m of s.matches){const key=m.stage+":"+m.round;if(!groups.has(key))groups.set(key,[]);groups.get(key).push(m);}
    const select=h("select",{class:"ucl-round","aria-label":"Lượt đấu"}),holder=h("div"),box=h("div",{class:"ucl-stack"},select,holder);
    options(select,[...groups].map(([key,m])=>[key,(phases[m[0].stage]||m[0].stage)+" · Lượt "+m[0].round]));
    const current=s.stage+":"+s.round;if(groups.has(current))select.value=current;
    function paint(){holder.replaceChildren(table(["Chủ nhà","Tỷ số","Khách"],groups.get(select.value).map(m=>[label(map,m.home),m.result?m.result.home+" – "+m.result.away+(m.result.pk_home!=null?" (pen "+m.result.pk_home+"–"+m.result.pk_away+")":""):"–",label(map,m.away)])));}
    select.addEventListener("change",paint);paint();await UI().sheet("Lịch thi đấu","",[UI().ok("Quay lại")],box);
  }
  async function scorers(status,kind){
    const doc=status.season[kind],map=names(status),title=kind==="goals"?"Vua phá lưới":"Kiến tạo";
    const rows=doc.rows.map(r=>[r.rank,r.name||"Cầu thủ chưa có tên",label(map,r.team_id),r[kind]]);
    const note=rows.length?(doc.coverage_complete?"":"Chỉ hiển thị các trận đã có dữ liệu cầu thủ."):"Chưa có dữ liệu cầu thủ được ghi nhận.";
    await UI().sheet(title,note,[UI().ok("Quay lại")],table(["#","Cầu thủ","CLB",kind==="goals"?"Bàn":"KT"],rows));
  }
  async function create(status){
    const h=UI().h,club=h("select",{"aria-label":"Câu lạc bộ"}),level=h("select",{"aria-label":"Độ khó"});
    options(club,status.teams.map(t=>[t.team_id,t.name||t.short||"Câu lạc bộ"]));options(level,status.levels.map(k=>[k,levels[k]||k]));level.value="NORMAL";
    const form=h("div",{class:"ucl-fields"},h("label",{},"Câu lạc bộ",club),h("label",{},"Độ khó",level),h("p",{class:"ucl-note"},"36 đội · 8 đối thủ · 4 trận sân nhà / 4 trận sân khách. Nhóm hạt giống theo sức mạnh trong game. Vòng loại trực tiếp đá một lượt; hòa đá hiệp phụ và luân lưu."));
    const agreed=await UI().sheet("Mùa UCL mới",status.season?"Mùa đang chọn sẽ được thay bằng mùa mới. Save My League thường được giữ nguyên.":"",[button("Hủy",false),button("Tạo mùa",true,"primary")],form);
    if(!agreed)return status;
    const seed=Date.now()%2147483647;
    return api({op:"create",team_id:Number(club.value),level:level.value,seed,draw:seed%status.draw_count,replace_season_uuid:status.season?.id});
  }
  async function open(){
    return UI().run("Đang mở UCL…",async()=>{
      let status=await api({op:"status"});
      while(true){
        const h=UI().h,s=status.season,map=names(status),box=h("div",{class:"ucl-stack"});
        box.append(h("div",{class:"ucl-status"},s?label(map,s.own)+" · "+(phases[s.stage]||s.stage)+" · Lượt "+s.round:"Chưa có mùa UCL"));
        if(s?.pending)box.append(h("p",{class:"ucl-note"},"Có trận đang chờ kết quả. Tiếp tục trận trước khi đổi chế độ."));
        const actions=[button("Đóng","close")];
        if(s){actions.push(button("Bảng xếp hạng","table"),button("Lịch đấu","fixtures"),button("Ghi bàn","goals"),button("Kiến tạo","assists"));}
        if(status.ready&&!s?.pending){actions.push(button("Mùa mới","create"));if(s)actions.push(button(status.enabled?"Về My League thường":"Chọn UCL",status.enabled?"leave":"activate","primary"));}
        if(!status.ready)box.append(h("p",{class:"ucl-note"},"Chế độ UCL chưa sẵn sàng trong bản này."));
        if(status.enabled)box.append(h("p",{class:"ucl-note"},"Vào game và mở My League để tiếp tục mùa UCL."));
        const action=await UI().sheet("UEFA Champions League","",actions,box);
        if(action==="close"||action==null||action===false)return;
        if(action==="table")await standings(status);else if(action==="fixtures")await fixtures(status);else if(action==="goals"||action==="assists")await scorers(status,action);else if(action==="create")status=await create(status);else status=await api({op:action});
      }
    });
  }
  window.UclPanel={open};
  document.addEventListener("DOMContentLoaded",()=>document.getElementById("private-ucl")?.addEventListener("click",open),{once:true});
})();
