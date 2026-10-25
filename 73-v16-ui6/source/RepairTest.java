import java.nio.file.*;import java.io.*;import java.security.*;import org.json.*;import org.efootballrevival.runtimeprobe.ModPayloadRepair;import android.content.Context;
public class RepairTest{
 static String sha(byte[] b)throws Exception{StringBuilder s=new StringBuilder();for(byte v:MessageDigest.getInstance("SHA-256").digest(b))s.append(String.format("%02x",v&255));return s.toString();}
 static JSONObject row(String name,byte[] b)throws Exception{return new JSONObject().put("path",name).put("bytes",b.length).put("sha256",sha(b));}
 static void check(boolean ok,String why){if(!ok)throw new AssertionError(why);}
 public static void main(String[] args)throws Exception{
  Path tmp=Files.createTempDirectory("ui6-repair-test-");Path assets=tmp.resolve("assets/gateway-release");Path root=tmp.resolve("root");Files.createDirectories(assets.resolve("work/tools"));Files.createDirectories(assets.resolve("livedata"));Files.createDirectories(root.resolve("work/tools"));
  byte[] code="original mod code".getBytes("UTF-8"),large=new byte[1048600];java.util.Arrays.fill(large,(byte)73);Files.write(assets.resolve("work/tools/test.py"),code);Files.write(assets.resolve("livedata/test.ucas"),large);
  JSONObject doc=new JSONObject().put("version","TEST-UI6").put("files",new JSONArray().put(row("work/tools/test.py",code)).put(row("livedata/test.ucas",large)));Path manifest=assets.resolve("ui6-runtime-manifest.json");Files.writeString(manifest,doc.toString());Path save=root.resolve("work/tools/myleague_editor.json");Files.writeString(save,"user edits");Context context=new Context(tmp.resolve("assets").toFile());ModPayloadRepair.ensure(context,root.toFile());check(Files.readAllBytes(root.resolve("livedata/test.ucas"))[0]==73,"missing payload not restored");
  long when=root.resolve("work/tools/test.py").toFile().lastModified();ModPayloadRepair.ensure(context,root.toFile());check(when==root.resolve("work/tools/test.py").toFile().lastModified(),"unchanged code rewritten");
  Files.write(root.resolve("work/tools/test.py"),"corrupt mod code!".getBytes("UTF-8"));ModPayloadRepair.ensure(context,root.toFile());check(java.util.Arrays.equals(code,Files.readAllBytes(root.resolve("work/tools/test.py"))),"small corruption not restored");
  large[0]=12;Files.write(root.resolve("livedata/test.ucas"),large);root.resolve("livedata/test.ucas").toFile().setLastModified(System.currentTimeMillis()+3000);ModPayloadRepair.ensure(context,root.toFile());check(Files.readAllBytes(root.resolve("livedata/test.ucas"))[0]==73,"changed large cached asset accepted");check(Files.readString(save).equals("user edits"),"mutable config overwritten");
  doc.put("files",new JSONArray().put(row("../escape",code)));Files.writeString(manifest,doc.toString());boolean blocked=false;try{ModPayloadRepair.ensure(context,root.toFile());}catch(IOException ex){blocked=true;}check(blocked,"path escape accepted");System.out.println("JAVA_REPAIR_PASS missing/corrupt/idempotent/large-cache/mutable/path");
 }
}
