package android.content.res;
import java.io.*;import java.util.*;
public class AssetManager {
 public File assets; public File overrideManifest; public String poison;public final List<String> opened=new ArrayList<>();
 public AssetManager(File assets){this.assets=assets;}
 public InputStream open(String name)throws IOException{
  opened.add(name);
  if(name.equals(poison))return new ByteArrayInputStream(new byte[]{0});
  if(overrideManifest!=null&&name.equals("gateway-release/ui6-runtime-manifest.json"))return new FileInputStream(overrideManifest);
  return new FileInputStream(new File(assets,name));
 }
}
