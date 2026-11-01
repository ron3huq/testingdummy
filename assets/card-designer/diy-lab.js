/* Standalone navigation overlay. Shared editor, images and validators stay intact. */
(() => {
  'use strict';
  const get = id => document.getElementById(id);
  if(new URLSearchParams(location.search).get('nativeInsets')==='host')document.documentElement.dataset.nativeInsets='host';
  document.body.classList.add('diy-lab');
  const shell = document.createElement('div');
  shell.id = 'labRoot';
  shell.innerHTML =
    '<section id="labHome" class="lab-page">' +
    '<div class="lab-home-top"><button id="labExit" aria-label="返回游戏主菜单">‹</button><div class="lab-brand"><span class="lab-eyebrow">DIY</span><h1>制卡工坊</h1></div><button id="labStatusOpen" class="lab-status-link" aria-label="新卡状态"><span class="lab-dot"></span><strong>新卡状态</strong></button><button id="labTrash">回收站</button></div>' +
    '<p class="lab-subtitle">把想象变成你的专属球员卡</p>' +
    '<button id="labNew" class="lab-create"><span>＋</span> 制作新卡</button>' +
    '<div id="labRecent" class="lab-recent" hidden><div class="lab-sec"><h2>继续编辑</h2></div><div id="labRecentRow" class="lab-recent-row"></div></div>' +
    '<div class="lab-library-heading"><h2 id="labLibraryTitle">我的作品</h2><span id="labCount" class="lab-count"></span><button id="labImport">导入工程</button></div>' +
    '<input id="labSearch" type="search" placeholder="搜索作品名称" aria-label="搜索作品">' +
    '<div id="labWorks" class="lab-work-grid"></div><p id="labHomeNote" role="status">正在加载本地作品…</p>' +
    '<p class="lab-disclaimer">作品与素材保存在本机 · 游戏版本 V16</p></section>' +
    '<section id="labEditor" class="lab-page" hidden>' +
    '<div class="lab-editor-top"><button id="labBack" aria-label="返回作品首页">‹</button><div class="lab-editor-title"><strong id="labTitle">新作品</strong><small id="labSaveState">本地草稿</small></div><button id="labUndo" aria-label="撤销">↶</button><button id="labSaveMenu" class="lab-primary">保存 / 入库</button></div>' +
    '<div id="labCanvas"><div id="labScene" class="lab-scene-tabs"></div><div id="labStageMount"></div><span id="labCanvasHint">单指移动 · 双指缩放旋转 · 图层工具可擦除</span></div>' +
    '<section id="labSheet" hidden><div class="lab-sheet-handle"></div><div class="lab-sheet-head"><strong id="labSheetTitle"></strong><button id="labSheetTall" type="button" aria-label="展开面板" aria-pressed="false"></button><button id="labSheetClose" aria-label="收起工具面板">完成</button></div><div id="labSubnav" hidden></div><div id="labPanelMount"></div></section>' +
    '<nav id="labDock" aria-label="制卡工具"></nav></section>' +
    '<section id="labStatus" class="lab-page" hidden><div class="lab-home-top"><button id="labStatusBack">‹ 返回</button><h1>新卡状态</h1></div><p class="lab-status-notice">资源准备、发卡入库与名单同步分别显示。新资源准备后需完全退出再进入游戏。</p><div id="labStatusList"></div></section>' +
    '<div id="labToast" role="status" aria-live="polite" hidden></div>' +
    '<dialog id="labActions" class="lab-dialog"><h2>保存与导出</h2><p>保存作品后，可检查资源并生成独立球员。</p><button id="labSave" class="lab-primary">保存作品</button><button id="labExportPng">导出当前画面 PNG</button><button id="labExportCard">导出全部作品工程</button><button id="labShareMore">工程备份与导入</button><button id="labGenerate" class="lab-primary">生成 / 入库与状态</button><button id="labActionsClose">返回编辑</button></dialog>' +
    '<dialog id="labDelete" class="lab-dialog"><h2>移入回收站？</h2><p id="labDeleteName"></p><p>作品与素材仍然保留，可恢复；不会释放游戏资源空间。</p><button id="labDeleteConfirm" class="lab-danger">确认移入回收站</button><button id="labDeleteCancel">取消</button></dialog>';
  document.body.append(shell);
  get('labExit').onclick=async()=>{try{await persist();if(window.AndroidCardDesigner)window.AndroidCardDesigner.closePanel();else toast('已返回作品首页；浏览器可关闭此页');}catch(e){toast(e.message);}};
  let page = 'home', trash = false, deleting = null, currentTool = null, noticeTimer;
  let toolMode = 'artwork', imagePart = 'import', lastArtworkTool = 'images';
  const parked = [];
  const homes = new Map();
  function toast(message) {
    get('labToast').textContent = message;
    get('labToast').hidden = false;
    clearTimeout(noticeTimer);
    noticeTimer = setTimeout(() => { get('labToast').hidden = true; }, 3200);
  }
  function library() {
    if (!state.diyTestLibrary) state.diyTestLibrary = {schema: 'diy-test-library/v1', trash: {}, updated: {}};
    const v = state.diyTestLibrary;
    if (v.schema !== 'diy-test-library/v1' || !v.trash || !v.updated) throw Error('作品目录版本不匹配，原数据保留');
    return v;
  }
  function name(key) { return state.players[key].diy?.name || '未命名草稿'; }
  async function persist() {
    const expected = revision;
    await save();
    if (savedRevision < expected) throw Error('保存尚未完成，请重试；本次操作未离开当前页面');
  }
  function route(next) {
    page = next;
    for (const [id, key] of [['labHome', 'home'], ['labEditor', 'editor'], ['labStatus', 'status']])
      get(id).hidden = next !== key;
    if (next !== 'editor') closeSheet();
    window.dispatchEvent(new Event('resize'));
  }
  function park(element) {
    if (!homes.has(element)) {
      const marker = document.createComment('standalone panel home');
      element.before(marker);
      homes.set(element, marker);
    }
    get('labPanelMount').append(element);
    parked.push(element);
  }
  function returnPanels() {
    for (const part of parked.splice(0)) homes.get(part).after(part);
  }
  function closeSheet() {
    returnPanels();
    currentTool = null;
    get('labSubnav').hidden = true;
    get('labSheet').hidden = true;
    get('labEditor').classList.remove('lab-sheet-open');
    for (const b of get('labDock').querySelectorAll('[data-tool]')) b.setAttribute('aria-pressed', 'false');
    window.dispatchEvent(new Event('resize'));
  }
  const artworkTools = [
    ['images', '图片', '＋', '图片与构图', 'cardArtworkPanel'],
    ['materials', '添加素材', '▧', '游戏球员素材', 'referenceMaterials'],
    ['background', '背景', '◈', '选择背景', 'backgroundPicker']
  ];
  const playerTools = [
    ['basics', '资料', '♙', '球员资料与模型', 'cardPlayerPanel'],
    ['abilities', '能力', '☷', '基础能力', 'cardPlayerPanel'],
    ['skills', '技能', '✧', '技能与增能', 'cardPlayerPanel']
  ];
  function configurePlayer(key) {
    const panel = get('cardPlayerPanel');
    const selectors = key === 'basics'
      ? '#diyName,#diyProfileSection,#diyPositionSection,#diyModelSection,#diyModelSearch,#diyModelQuery,#diyPersonalizationSection'
      : key === 'abilities' ? '#diyAbilitySection' : '#diySkillSection,#diyBoosterSection';
    for (const child of panel.children) {
      const visible = child.matches(selectors) || Boolean(child.querySelector(selectors)) || child.id === 'diyPlayerStatus';
      child.classList.toggle('lab-player-hidden', !visible);
    }
    panel.dataset.labPlayer = key;
    for (const id of key === 'abilities' ? ['diyAbilitySection'] : key === 'skills' ? ['diySkillSection'] : [])
      get(id).open = true;
  }
  function showImagePart(next) {
    returnPanels();
    imagePart = next;
    const part = next === 'layers' ? get('artTools')
      : next === 'compose' ? document.querySelector('main .controls') : get('cardArtworkPanel');
    if (!part) throw Error('图片工具尚未就绪');
    park(part);
    get('labPanelMount').dataset.imagePart = next;
    for (const b of get('labSubnav').children) b.setAttribute('aria-pressed', String(b.dataset.imagePart === next));
    window.dispatchEvent(new Event('resize'));
  }
  function imageNavigation() {
    get('labSubnav').replaceChildren();
    for (const [key, label] of [['import', '导入图片'], ['compose', '构图调整'], ['layers', '图层操作']]) {
      const b = document.createElement('button');
      b.dataset.imagePart = key;
      b.textContent = label;
      b.onclick = () => showImagePart(key);
      get('labSubnav').append(b);
    }
    get('labSubnav').hidden = false;
    showImagePart(imagePart);
  }
  function renderDock() {
    const dock = get('labDock');
    dock.replaceChildren();
    get('labEditor').dataset.toolMode = toolMode;
    for (const [key, label, icon] of toolMode === 'player' ? playerTools : artworkTools) {
      const b = document.createElement('button');
      b.dataset.tool = key;
      b.setAttribute('aria-pressed', String(currentTool === key));
      const mark = document.createElement('span');
      mark.textContent = icon;
      const title = document.createElement('small');
      title.textContent = label;
      b.append(mark, title);
      b.onclick = () => openTool(key);
      dock.append(b);
    }
    const master = document.createElement('button');
    master.id = 'labModeSwitch';
    master.className = 'lab-mode-switch';
    master.setAttribute('aria-pressed', String(toolMode === 'player'));
    master.setAttribute('aria-label', toolMode === 'player' ? '返回图片与背景工具' : '切换到球员工具');
    master.innerHTML = '<span>' + (toolMode === 'player' ? '▧' : '♙') + '</span><small>' +
      (toolMode === 'player' ? '返回制图' : '球员') + '</small>';
    master.onclick = () => {
      closeSheet();
      toolMode = toolMode === 'player' ? 'artwork' : 'player';
      renderDock();
      openTool(toolMode === 'player' ? 'basics' : lastArtworkTool);
    };
    dock.append(master);
  }
  function openTool(key) {
    if (currentTool === key) { closeSheet(); return; }
    closeSheet();
    const item = (toolMode === 'player' ? playerTools : artworkTools).find(t => t[0] === key);
    if (!item) return;
    const part = get(item[4]);
    if (!part) { toast('工具尚未就绪，请重试'); return; }
    window.cardChooseTool(toolMode === 'player' ? 'player' : key === 'background' ? 'background' : 'canvas');
    if (toolMode === 'player') configurePlayer(key);
    else lastArtworkTool = key;
    if (key === 'images') imageNavigation();
    else {
      park(part);
      if (key === 'background') park(get('suitePicker'));
      delete get('labPanelMount').dataset.imagePart;
    }
    if (key === 'materials') {
      // Keep the existing action outside the scrolling material list.
      park(get('materialAdd'));
      get('labSheetClose').before(get('materialAdd'));
      part.open = true;
      part.dispatchEvent(new Event('toggle'));
    }
    currentTool = key;
    get('labSheetTitle').textContent = item[3];
    get('labSheet').hidden = false;
    get('labEditor').classList.add('lab-sheet-open');
    get('labDock').querySelector('[data-tool="' + key + '"]').setAttribute('aria-pressed', 'true');
    window.dispatchEvent(new Event('resize'));
  }
  renderDock();
  function openWork(key) {
    if (!state.players[key] || library().trash[key]) return;
    player = key;
    scene = 'detail';
    selected = 0;
    get('player').value = key;
    sync();
    toolMode = 'artwork';
    renderDock();
    route('editor');
    closeSheet();
  }
  let renderEpoch = 0;
  async function renderHome() {
    if (!state) return;
    const epoch = ++renderEpoch, q = get('labSearch').value.trim().toLowerCase(), meta = library();
    const keys = Object.keys(state.players).filter(k => Boolean(meta.trash[k]) === trash && name(k).toLowerCase().includes(q));
    get('labWorks').replaceChildren();
    get('labLibraryTitle').textContent = trash ? '回收站' : '我的作品';
    get('labTrash').textContent = trash ? '返回作品' : '回收站';
    get('labNew').hidden = trash;
    get('labImport').hidden = trash;
    get('labHomeNote').textContent = keys.length ? '点击卡面继续编辑' : trash ? '回收站为空' : q ? '没有匹配的作品' : '从制作新卡开始你的第一张作品';
    get('labCount').textContent = keys.length ? String(keys.length) : '';
    get('labRecentRow').replaceChildren();
    get('labRecent').hidden = trash || q !== '' || keys.length < 2;
    for (const key of keys) {
      const card = document.createElement('article');
      card.className = 'lab-work';
      card.dataset.work = key;
      const edit = document.createElement('button');
      edit.className = 'lab-work-edit';
      edit.disabled = trash;
      edit.setAttribute('aria-label', '编辑 ' + name(key));
      const preview = document.createElement('div');
      preview.className = 'lab-work-preview';
      const image = document.createElement('img');
      image.alt = name(key);
      preview.append(image);
      const badge = document.createElement('span');
      badge.className = 'lab-work-badge';
      badge.textContent = trash ? '已移入回收站' : '草稿';
      preview.append(badge);
      const title = document.createElement('strong');
      title.textContent = name(key);
      const hint = document.createElement('small');
      hint.textContent = trash ? '身份与素材保留' : '详细卡面 · 点击编辑';
      edit.append(preview, title, hint);
      edit.onclick = () => openWork(key);
      const action = document.createElement('button');
      action.className = 'lab-work-action';
      action.textContent = trash ? '恢复作品' : '移入回收站';
      action.onclick = () => {
        if (trash) restore(key);
        else {
          deleting = key;
          get('labDeleteName').textContent = name(key);
          get('labDelete').showModal();
        }
      };
      card.append(edit, action);
      get('labWorks').append(card);
      try {
        for (const layer of state.players[key].detail) if (layer.visible) await readyImage(layer.asset);
        if (epoch !== renderEpoch) return;
        const thumb = document.createElement('canvas');
        thumb.width = 256;
        thumb.height = 360;
        const paint = thumb.getContext('2d');
        drawScene(paint, key, 'detail');
        paint.globalCompositeOperation = 'destination-over';
        paint.save();
        paint.scale(thumb.width / 512, thumb.height / canvasHeight(key, 'detail'));
        window.CardSuites?.drawBase(paint, key, 'detail');
        paint.restore();
        paint.globalCompositeOperation = 'source-over';
        paint.save();
        paint.scale(thumb.width / 512, thumb.height / canvasHeight(key, 'detail'));
        window.CardSuites?.drawFrame(paint, key, 'detail');
        paint.restore();
        image.src = thumb.toDataURL();
        if (!get('labRecent').hidden && keys.indexOf(key) >= keys.length - 6) {
          const chip = document.createElement('button');
          chip.className = 'lab-recent-card';
          chip.setAttribute('aria-label', '继续编辑 ' + name(key));
          const pic = document.createElement('img');
          pic.alt = '';
          pic.src = image.src;
          const cap = document.createElement('span');
          cap.textContent = name(key);
          chip.append(pic, cap);
          chip.onclick = () => openWork(key);
          get('labRecentRow').prepend(chip);
        }
      } catch (_) { preview.classList.add('lab-preview-unavailable'); image.hidden = true; }
    }
  }
  async function restore(key) {
    const original = library().trash[key];
    if (!original) return;
    try {
      delete library().trash[key];
      changed();
      await persist();
      await renderHome();
      toast('已恢复作品，原身份与素材保持');
    } catch (e) {
      library().trash[key] = original;
      changed();
      toast(e.message);
    }
  }
  get('labDeleteConfirm').onclick = async () => {
    const key = deleting, button = get('labDeleteConfirm');
    if (!key || !state.players[key] || button.disabled) return;
    button.disabled = true;
    try {
      library().trash[key] = {at: new Date().toISOString()};
      changed();
      await persist();
      get('labDelete').close();
      await renderHome();
      toast('已移入回收站，作品与素材保留');
    } catch (e) {
      delete library().trash[key];
      changed();
      toast(e.message);
    } finally { button.disabled = false; }
  };
  get('labDeleteCancel').onclick = () => get('labDelete').close();
  async function goHome() {
    try { await persist(); trash = false; route('home'); await renderHome(); }
    catch (e) { toast(e.message); }
  }
  get('labBack').onclick = goHome;
  get('labTrash').onclick = () => { trash = !trash; renderHome().catch(e => toast(e.message)); };
  get('labSearch').oninput = () => renderHome().catch(e => toast(e.message));
  get('labNew').onclick = () => {
    const before = new Set(Object.keys(state.players)), d = get('diyCreatePlayerDialog');
    get('diyCreatePlayer').click();
    d.addEventListener('close', () => {
      const created = Object.keys(state.players).find(k => !before.has(k));
      if (created) openWork(created);
      renderHome().catch(e => toast(e.message));
    }, {once: true});
  };
  get('labImport').onclick = () => get('importProject').click();
  get('labSheetClose').onclick = closeSheet;
  get('labSheetTall').onclick = () => {
    const tall = get('labEditor').classList.toggle('lab-sheet-tall');
    get('labSheetTall').setAttribute('aria-pressed', String(tall));
    get('labSheetTall').setAttribute('aria-label', tall ? '收起面板' : '展开面板');
    window.dispatchEvent(new Event('resize'));
  };
  get('labUndo').onclick = () => get('undo').click();
  get('labSaveMenu').onclick = () => get('labActions').showModal();
  get('labActionsClose').onclick = () => get('labActions').close();
  get('labSave').onclick = async () => {
    try { await persist(); get('labActions').close(); toast('作品已保存到本机'); }
    catch (e) { toast(e.message); }
  };
  get('labExportPng').onclick = () => { get('labActions').close(); get('export').click(); };
  get('labExportCard').onclick = () => { get('labActions').close(); get('saveProject').click(); };
  get('labShareMore').onclick = () => {
    get('labActions').close();
    closeSheet();
    park(get('cardSharePanel'));
    get('labSheetTitle').textContent = '工程备份与分享';
    get('labSheet').hidden = false;
    get('labEditor').classList.add('lab-sheet-open');
    window.dispatchEvent(new Event('resize'));
  };
  function openGeneration() {
    get('labActions').close(); closeSheet(); route('status');
    get('diyGeneration').classList.remove('lab-player-hidden');
    park(get('diyGeneration')); get('labStatusList').append(get('diyGeneration'));
    get('diyGenerationRefresh').click();
  }
  get('labStatusOpen').onclick = openGeneration;
  get('labGenerate').onclick = openGeneration;
  get('diyImportShortcut').onclick = openGeneration;
  get('labStatusBack').onclick = goHome;
  window.DiyLab = {
    openWork, openTool, goHome, refreshHome:renderHome, persist, notify:toast,
    async back() {
      const d = [...document.querySelectorAll('dialog[open]')].pop();
      if (d) { d.close(); return; }
      if (!get('labSheet').hidden) { closeSheet(); return; }
      if (page !== 'home') { await goHome(); return; }
      try { await persist(); window.AndroidCardDesigner?.closePanel(); }
      catch (e) { toast(e.message); }
    }
  };
  let attempts = 0;
  const boot = setInterval(() => {
    if (typeof state === 'undefined' || !state || !window.CardSuites?.catalog) {
      if (++attempts > 400) { clearInterval(boot); get('labHomeNote').textContent = '启动资源未就绪，请关闭并重新进入；已有作品保留。'; }
      return;
    }
    clearInterval(boot);
    try {
      library();
      get('diyGeneration').classList.remove('lab-player-hidden');
      const stage = document.querySelector('main > section[data-phone-part="canvas"]');
      if (!stage) throw Error('画布模块未就绪');
      get('labStageMount').append(stage);
      get('suitePicker').querySelector('h2').textContent = '背景套装';
      for (const id of ['smallTab', 'detailTab']) get('labScene').append(get(id));
      const oldSync = sync;
      sync = function () {
        oldSync();
        get('labTitle').textContent = name(player);
        get('labSaveState').textContent = savedRevision >= revision ? '已保存 · 本地草稿' : '正在保存…';
      };
      new MutationObserver(() => {
        get('labSaveState').textContent = get('saveStatus').textContent;
      }).observe(get('saveStatus'), {childList: true, characterData: true, subtree: true});
      get('diyName').addEventListener('change', () => {
        get('labTitle').textContent = name(player);
      });
      scene = 'detail';
      get('guides').checked = false;
      sync();
      renderHome().catch(e => toast(e.message));
      document.documentElement.dataset.diyLabReady = 'true';
      document.documentElement.classList.remove('lab-boot');
      route('home');
    } catch (e) { get('labHomeNote').textContent = '启动失败：' + e.message; }
  }, 50);
})();
