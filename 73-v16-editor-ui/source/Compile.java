import javax.tools.*;class Compile {public static void main(String[] a){int code=ToolProvider.getSystemJavaCompiler().run(null,null,null,a);if(code!=0)System.exit(code);}}
