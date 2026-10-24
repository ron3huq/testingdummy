"""Apply isolated launcher UI edits to a disassembled 73 V16 classes5.dex.
Timer/editor/native extensions are separate changes, not claimed by this patch.
"""
from pathlib import Path
import re
ROOT=Path('/workspace/ronaldo-work/73-ui/smali/org/efootballrevival/runtimeprobe')
p=ROOT/'UiStrings.smali';s=p.read_text()
s=re.sub(r'(\.method public static setLanguage\(Ljava/lang/String;\)V).*?\.end method',r'''\1
    .registers 2
    const/4 v0, 0x1
    sput-boolean v0, Lorg/efootballrevival/runtimeprobe/UiStrings;->english:Z
    return-void
.end method''',s,flags=re.S)
s=s.replace('    invoke-static {v1}, Lorg/efootballrevival/runtimeprobe/UiStringsData;->templates(Ljava/util/List;)V','    invoke-static {v1}, Lorg/efootballrevival/runtimeprobe/UiStringsData;->templates(Ljava/util/List;)V\n\n    const/4 v0, 0x1\n    sput-boolean v0, Lorg/efootballrevival/runtimeprobe/UiStrings;->english:Z')
p.write_text(s)
p=ROOT/'GatewayBootActivity.smali';s=p.read_text()
# Change only this screen's known theme constants; leave control callbacks intact.
for a,b in {'-0xe6e5db':'-0xf4eddf','-0xdad9c8':'-0xece3cf','-0x8baf64':'-0xe54e5a','0x337d62ab':'0x331ab1a6'}.items():s=s.replace(a,b)
start=s.index('.method private button(');end=s.index('.end method',start);block=s[start:end];assert 'return-object v0' in block
block=block.replace('    return-object v0','    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->styleEnter(Landroid/widget/Button;)V\n\n    return-object v0');s=s[:start]+block+s[end:]
s+='''
.method private styleEnter(Landroid/widget/Button;)V
    .registers 4
    invoke-virtual {p1}, Landroid/widget/Button;->getText()Ljava/lang/CharSequence;
    move-result-object v0
    invoke-interface {v0}, Ljava/lang/CharSequence;->toString()Ljava/lang/String;
    move-result-object v0
    const-string v1, "Enter Game"
    invoke-virtual {v1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v0
    if-eqz v0, :done
    invoke-virtual {p1}, Landroid/widget/Button;->getMinimumHeight()I
    move-result v0
    mul-int/lit8 v0, v0, 0x2
    invoke-virtual {p1, v0}, Landroid/widget/Button;->setMinimumHeight(I)V
    const/high16 v0, 0x41b00000
    invoke-virtual {p1, v0}, Landroid/widget/Button;->setTextSize(F)V
    :done
    return-void
.end method
'''
p.write_text(s)
print('English default and launcher-only theme/Enter sizing patched')
