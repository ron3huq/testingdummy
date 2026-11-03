import java.io.*;import java.nio.file.*;import java.security.*;import java.util.*;import org.json.*;
import android.content.Context;import android.content.res.AssetManager;import org.efootballrevival.runtimeprobe.ModPayloadRepair;
public class TestInstall{
 static void check(boolean b,String message){if(!b)throw new AssertionError(message);}
 static byte[] read(File p)throws Exception{return Files.readAllBytes(p.toPath());}
 static String sha(File p)throws Exception{byte[] hash=MessageDigest.getInstance("SHA-256").digest(read(p));StringBuilder s=new StringBuilder();for(byte b:hash)s.append(String.format("%02x",b&255));return s.toString();}
 public static void main(String[]args)throws Exception{
 File work=new File(args[0]),payload=new File(work,"payload");File root=new File(work,"installer-fixture");root.mkdirs();
 File db=new File(root,"outputs/efootball/local-club.sqlite3");db.getParentFile().mkdirs();byte[] sentinel="SYNTHETIC-SAVE-SENTINEL".getBytes("UTF-8");Files.write(db.toPath(),sentinel);
 AssetManager assets=new AssetManager(new File("/workspace/work/full8-rc2/payload/assets"));Context ctx=new Context(assets);
 assets.overrideManifest=new File("/workspace/work/full8-rc2/payload/assets/gateway-release/ui6-runtime-manifest.json");boolean reproduced=false;
 try{ModPayloadRepair.ensure(ctx,root);}catch(FileNotFoundException e){reproduced=e.getMessage().contains("__pycache__/appearance_choices.cpython-312.pyc");}
 check(reproduced,"Original RC2 missing asset was not reproduced");System.out.println("ORIGINAL_RC2_MISSING_CACHE_REPRODUCED");
 assets.overrideManifest=null;assets.assets=new File(payload,"assets");assets.opened.clear();ModPayloadRepair.ensure(ctx,root);check(Arrays.equals(sentinel,read(db)),"Save changed on upgrade");System.out.println("HF1_UPGRADE_FROM_FAILED_RC2_PASSED");
 File cold=new File(work,"installer-fresh");cold.mkdirs();assets.opened.clear();ModPayloadRepair.ensure(ctx,cold);
 JSONObject manifest=new JSONObject(new String(read(new File(payload,"assets/gateway-release/ui6-runtime-manifest.json")),"UTF-8"));JSONArray rows=manifest.getJSONArray("files");
 for(int i=0;i<rows.length();i++){JSONObject row=rows.getJSONObject(i);String path=row.getString("path");check(!path.contains("__pycache__"),"Cache requested");check(assets.opened.contains("gateway-release/"+path),"Asset was not opened "+path);check(sha(new File(cold,path)).equals(row.getString("sha256")),"Installed hash mismatch "+path);}
 System.out.println("FRESH_INSTALL_ALL_"+rows.length()+"_ASSET_OPENS_AND_HASHES_PASSED");
 assets.opened.clear();ModPayloadRepair.ensure(ctx,root);check(assets.opened.size()==1,"Unchanged install unexpectedly reopened resource assets");
 String rel="work/tools/libsingle_player.so";File target=new File(root,rel);byte[] original=read(target),corrupted=original.clone();corrupted[20]^=1;Files.write(target.toPath(),corrupted);
 assets.poison="gateway-release/"+rel;boolean rejected=false;
 try{ModPayloadRepair.ensure(ctx,root);}catch(IOException e){rejected=e.getMessage().contains("verification failed");}
 check(rejected,"Corrupt source bypassed integrity");check(Arrays.equals(corrupted,read(target)),"Failed repair replaced target");assets.poison=null;ModPayloadRepair.ensure(ctx,root);check(Arrays.equals(original,read(target)),"Valid repair failed");check(Arrays.equals(sentinel,read(db)),"Save changed during repair");
 JSONObject result=new JSONObject();for(String key:new String[]{"passed","original_RC2_FileNotFoundException_reproduced","upgrade_from_failed_install","fresh_install_all_assets_opened","warm_reopen","tampered_source_rejected","corrupted_native_file_repaired","synthetic_save_preserved","original_Java_installer_source_executed"})result.put(key,true);result.put("runtime_asset_count",rows.length());result.put("Android_AssetManager_replaced_by_filesystem_adapter",true);result.put("phone_verified",false);Files.write(new File(work,"installer-validation.json").toPath(),result.toString(2).getBytes("UTF-8"));System.out.println(result.toString(2));
 }
}
