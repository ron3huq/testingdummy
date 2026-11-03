package android.content;
import android.content.res.AssetManager;
public class Context{private final AssetManager assets;public Context(AssetManager assets){this.assets=assets;}public AssetManager getAssets(){return assets;}}
