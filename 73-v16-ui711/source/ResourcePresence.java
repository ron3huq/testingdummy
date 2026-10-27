package org.efootballrevival.runtimeprobe;
import java.io.*;import org.json.*;
public final class ResourcePresence{
 public static boolean check(File root,ResourceInstaller.Plan plan,long version){int required=0,present=0;JSONArray missing=new JSONArray();try{
  for(ResourceInstaller.Item item:plan.items.values()){
   if(!item.path.startsWith("assetpacks/"))continue;required++;String[] parts=item.path.split("/",5);if(parts.length!=5||!parts[2].matches("[0-9]+")||!parts[3].matches("[0-9]+"))throw new IOException("Invalid asset pack path");String active=parts[0]+"/"+parts[1]+"/"+version+"/"+parts[3]+"/"+parts[4];File file=new File(root,active);if(file.isFile()&&file.length()==item.bytes)present++;else if(missing.length()<24)missing.put(new JSONObject().put("path",active).put("expected_bytes",item.bytes).put("actual_bytes",file.isFile()?file.length():-1));
  }
  JSONObject doc=new JSONObject().put("version","73-ui7.4").put("app_version_code",version).put("required_asset_pack_files",required).put("present_with_expected_size",present).put("missing_or_wrong_size",missing).put("mutable_Download_files_checked",false);File target=new File(root,"embedded-gateway/work/tools/resource-presence-status.json");try{if(target.getParentFile().isDirectory()){File temp=new File(target.getParentFile(),"resource-presence-status.tmp");try(FileOutputStream out=new FileOutputStream(temp)){out.write(doc.toString(2).getBytes("UTF-8"));}if(!temp.renameTo(target))temp.delete();}}catch(Exception ignored){}
  return required>0&&present==required;
 }catch(Exception ex){return false;}}
}
