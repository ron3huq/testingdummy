RONALDO 2017 / 2014 - BLENDER REPAIR V3

Mo .blend bang Blender 4.3 tro len. Texture da pack; khong can addon FMDL.
Day la FILE NGUON BLENDER, KHONG phai goi cai Android/work/livedata.

2017:
- Giu mat nen 2006, giu topology/UV/weight; sculpt nhe ham, ma duoi va
  vung duoi cam theo anh tham khao. Dich chuyen lon nhat duoi 6 mm.
- Giu toc tu ronaldo2017.rar. Khong nhap mesh mat 2017 cu.
- Mesh/UV/normal/weight da dau-gay 2006 goc giu nguyen.
- Bo cach chuyen UV theo dinh gan nhat; bake mau nguon theo tung texel
  len UV 2006. Lam sach mau toc cu o thai duong, feather vung noi.

2014:
- Bo prototype dang mu va cac ong duong ke noi cua ban cu.
- Dung toc 2013 goc nguoi dung da cung cap, chinh nguoc huong duong ngoi,
  ha mai, vuot lech va om gon phan sau theo anh 2014. Giu mat nen 2006.
- Chi tiet toc cat sat hai ben duoc chuyen tu nguon 2017, bake vao UV
  2006, kem duong ngoi va hai vet cao. Khong dung mot mang mau phang.
- Khong phai mesh 2014 trich tu ronaldo2014.rar: RAR chi chua anh.
- Toc chi dung hair cards nguon; khong con hang trieu dinh soi procedural.

Cac vet cao nam trong *_Scalp_SeamMatched_BAKED.png va mot phan
*_Face_Temples_Clean_BAKED.png, KHONG phai object duong noi.
*_HairMask_BAKED.png la mask phi mau de tach do bong toc voi da.
Cac vet cao da hien trong render Blender. De hien trong game, phai
cook/retarget mesh va gan dung UV, diffuse va mask vao material Android.
Khong chi export FBX roi mong shader Blender tu chuyen sang shader game.
Shader masked/diffuse cua toc 2014 la preview Blender, can tao lai material
engine khi port. Giu alpha cua texture toc, khong bien no thanh opaque.

Ten SCALP_NATIVE_2006 trong scene chi mesh nguon PC 2006 goc, KHONG
co nghia mesh nay da la asset native Android. Rig la PES tham chieu.
Cac bai test mo lai file/UV/weight/texture/pose KHONG chung minh GPU
Android het mat den hay cutscene khong loi. device_verified = false.

Preview mat/mi/nhan cau dung chung van thieu mot so texture engine tu
bo Blender 2006 goc. Ban nay khong doi mat de che han che do.
Nguon toc 2013: bo nguon Super Games v12 do nguoi dung cung cap;
2017: ronaldo2017.rar nguoi dung cung cap. Giu credit cua tac gia goc.

Rebuild trong workspace:
1. Giai nen bo Blender 2006 goc vao /workspace/ronaldo-work/input-0/.
2. Can reader FmdlFile tu pes-fmdl-blender commit
   231093d3a056176b8d6e33e79d13f5563b27b985.
3. Doc build.py de gan lai duong dan cac nguon 2017 va 2013/converted.
4. Blender -b Ronaldo_2006_EDIT.blend --python build.py -- 2017
   Blender -b Ronaldo_2006_EDIT.blend --python build.py -- 2014
5. Blender -b Ronaldo_2014_REPAIR_V3.blend --python refine_hair_2014.py
6. Chay validate.py; render_five_views.py neu can xuat lai anh.
