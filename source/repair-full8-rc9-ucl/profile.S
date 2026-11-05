.text
.global rc8_profile
.global rc8_configure
rc8_profile:
 movz x16, #(89138556572074 & 65535)
 movk x16, #((89138556572074 >> 16) & 65535), lsl #16
 movk x16, #((89138556572074 >> 32) & 65535), lsl #32
 cmp x0,x16
 b.ne original
 adrp x0, rc8_name
 add x0,x0,#0
 ret
original:
 mov x8,#0xf806
 b old_profile_continue
rc8_configure:
 sub w16,w0,#1
 cmp w16,#5
 b.hi invalid
 add w17,w0,#48
 adrp x16,rc8_name
 strb w17,[x16,#3]
 mov w0,#1
 ret
invalid:
 mov w0,#0
 ret
