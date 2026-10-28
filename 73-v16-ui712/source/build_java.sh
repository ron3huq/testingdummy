set -e
p=/workspace/73-ui712/build
mkdir -p "$p/java-out" "$p/new-dex"
java /workspace/ronaldo-work/73-ui/Compile.java -source 8 -target 8 -classpath /workspace/73-ui712/build/stubs-out:/workspace/ronaldo-work/73-ui/android.jar:/workspace/ronaldo-work/73-ui/json.jar:/workspace/ronaldo-work/73-ui74/nanohttpd.jar:/workspace/ronaldo-work/73-ui77/stubs-out -d "$p/java-out" "$p"/java/org/efootballrevival/runtimeprobe/*.java
find "$p/java-out" -name '*.class' > "$p/java-classes.list"
java -cp /workspace/ronaldo-work/73-ui/r8.jar com.android.tools.r8.D8 --min-api 24 --lib /workspace/ronaldo-work/73-ui/android.jar --output "$p/new-dex" @"$p/java-classes.list"
java -cp /workspace/ronaldo-work/73-ui/apktool.jar /workspace/ronaldo-work/73-ui/DexTool.java d "$p/apk/classes5.dex" "$p/smali"
java -cp /workspace/ronaldo-work/73-ui/apktool.jar /workspace/ronaldo-work/73-ui/DexTool.java d "$p/new-dex/classes.dex" "$p/helper-smali"
python /workspace/73-ui712/merge_dex.py
java -cp /workspace/ronaldo-work/73-ui/apktool.jar /workspace/ronaldo-work/73-ui/DexTool.java a "$p/smali" "$p/classes5-ui712.dex"
