package org.efootballrevival.runtimeprobe;
import java.text.Normalizer;import java.util.Locale;
public final class EditorSearch {
 private static final ThreadLocal<Query> last=new ThreadLocal<>();
 private static final class Query{final String raw;final String[] tokens;Query(String s){raw=s;String n=fold(s.trim());tokens=n.isEmpty()?new String[0]:n.split("\\s+");}}
 public static String fold(String value){
  if(value==null||value.isEmpty())return "";String lower=value.toLowerCase(Locale.ROOT);boolean ascii=true;for(int i=0;i<lower.length();i++)if(lower.charAt(i)>127){ascii=false;break;}if(ascii)return lower;
  String n=Normalizer.normalize(lower,Normalizer.Form.NFD);StringBuilder b=new StringBuilder(n.length());
  for(int i=0;i<n.length();i++){char c=n.charAt(i);int t=Character.getType(c);if(t==Character.NON_SPACING_MARK||t==Character.COMBINING_SPACING_MARK||t==Character.ENCLOSING_MARK)continue;
   switch(c){case '\u0111':case '\u00f0':b.append('d');break;case '\u0142':b.append('l');break;case '\u00f8':b.append('o');break;case '\u00df':b.append("ss");break;case '\u00e6':b.append("ae");break;case '\u0153':b.append("oe");break;case '\u0131':b.append('i');break;default:b.append(c);}}
  return b.toString();
 }
 public static String[] tokens(String query){Query q=last.get();if(q==null||!q.raw.equals(query)){q=new Query(query);last.set(q);}return q.tokens;}
 public static boolean textMatches(String[] tokens,String prepared){for(String word:tokens)if(!prepared.contains(word))return false;return true;}
 public static boolean matchesPrepared(String query,String prepared,int mode,boolean current,boolean squad,boolean warehouse){if(mode==1&&!current||mode==2&&!squad||mode==3&&!warehouse||mode==4&&(squad||warehouse))return false;return textMatches(tokens(query),prepared);}
 public static boolean matches(String query,String text,int mode,boolean current,boolean squad,boolean warehouse){return matchesPrepared(query,fold(text),mode,current,squad,warehouse);}
 public static boolean catalogMatches(String query,String text,int position,int candidatePosition,String type,String candidateType){return(position<0||position==candidatePosition)&&(type.isEmpty()||type.equals(candidateType))&&matches(query,text,0,false,false,false);}
}
