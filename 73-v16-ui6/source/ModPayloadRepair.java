package org.efootballrevival.runtimeprobe;
import android.content.Context;import java.io.*;import java.security.MessageDigest;import org.json.*;
public final class ModPayloadRepair {
 private static String digest(File file)throws Exception{MessageDigest d=MessageDigest.getInstance("SHA-256");try(InputStream in=new FileInputStream(file)){byte[] b=new byte[65536];int n;while((n=in.read(b))>0)d.update(b,0,n);}StringBuilder out=new StringBuilder();for(byte v:d.digest())out.append(String.format(java.util.Locale.ROOT,"%02x",v&255));return out.toString();}
 private static byte[] read(InputStream in)throws IOException{try(InputStream stream=in;ByteArrayOutputStream out=new ByteArrayOutputStream()){byte[] b=new byte[8192];int n;while((n=stream.read(b))>0)out.write(b,0,n);return out.toByteArray();}}
 // All functional UI6 overrides are verified by ensure() before Python starts.
 // Existing unchanged-size base assets need no duplicate extraction on upgrade.
 public static boolean keepExisting(File file,JSONObject row)throws Exception{return file.isFile()&&file.length()==row.getLong("bytes");}
 public static void ensure(Context context,File root)throws Exception{
  JSONObject doc=new JSONObject(new String(read(context.getAssets().open("gateway-release/ui6-runtime-manifest.json")),"UTF-8"));JSONArray rows=doc.getJSONArray("files");String prefix=root.getCanonicalPath()+File.separator;
  File cacheFile=new File(root,".ui6-runtime-cache.json");JSONObject prior;
  try{prior=new JSONObject(new String(read(new FileInputStream(cacheFile)),"UTF-8"));if(!doc.getString("version").equals(prior.optString("version")))prior=new JSONObject();}catch(Exception ex){prior=new JSONObject();}
  JSONObject previous=prior.optJSONObject("files");JSONObject cached=new JSONObject();
  for(int i=0;i<rows.length();i++){
   JSONObject row=rows.getJSONObject(i);String name=row.getString("path"),sha=row.getString("sha256");long size=row.getLong("bytes");File target=new File(root,name);
   if(!target.getCanonicalPath().startsWith(prefix))throw new IOException("Invalid mod resource path");
   JSONObject item=previous==null?null:previous.optJSONObject(name);boolean valid=target.isFile()&&target.length()==size;
   // Small code/metadata is always hashed. Large local resources reuse only
   // a cache made after hash verification, tied to release, size and mtime.
   boolean cachedHash=valid&&size>1048576&&item!=null&&sha.equals(item.optString("sha256"))&&item.optLong("mtime",-1)==target.lastModified()&&item.optLong("bytes",-1)==size;
   if(valid&&!cachedHash)valid=sha.equals(digest(target));
   if(!valid){
    File parent=target.getParentFile();if(!parent.isDirectory()&&!parent.mkdirs())throw new IOException("Cannot prepare mod folder");File temp=File.createTempFile("ui6-", ".tmp",parent);
    try{
     try(InputStream in=context.getAssets().open("gateway-release/"+name);FileOutputStream out=new FileOutputStream(temp)){byte[] b=new byte[65536];int n;while((n=in.read(b))>0)out.write(b,0,n);out.getFD().sync();}
     if(temp.length()!=size||!sha.equals(digest(temp)))throw new IOException("Mod resource verification failed: "+name);
     if(!temp.renameTo(target))throw new IOException("Cannot restore mod resource: "+name);
    }finally{if(temp.exists())temp.delete();}
   }
   JSONObject stamp=new JSONObject();stamp.put("sha256",sha);stamp.put("bytes",size);stamp.put("mtime",target.lastModified());cached.put(name,stamp);
  }
  JSONObject next=new JSONObject();next.put("version",doc.getString("version"));next.put("files",cached);try(FileOutputStream out=new FileOutputStream(cacheFile)){out.write(next.toString().getBytes("UTF-8"));}
 }
}
