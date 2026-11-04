// Preserve original FULL-7 code/state; add before/after hooks around apply_base.
.text
.p2align 4
.extern callbacks
.extern original_apply_tail
.extern original_apply_ret
.extern original_rating_tail
.global rc6_configure
rc6_configure:
 adrp x8,callbacks
 add x8,x8,:lo12:callbacks
 str x2,[x8,#16]
 str x1,[x8,#8]
 stlr x0,[x8]
 ret
.global rc6_apply
rc6_apply:
 cbnz w1,rc6_original_apply
 cbz x0,rc6_original_apply
 cbz x2,rc6_original_apply
 sub sp,sp,#64
 stp x29,x30,[sp]
 mov x29,sp
 stp x0,x1,[sp,#16]
 str x2,[sp,#32]
 str wzr,[sp,#40]
 adrp x8,callbacks
 add x8,x8,:lo12:callbacks
 ldar x8,[x8]
 cbz x8,1f
 mov x1,x2
 blr x8
 str w0,[sp,#40]
1:
 ldp x0,x1,[sp,#16]
 ldr x2,[sp,#32]
 bl rc6_original_apply
 ldr x0,[sp,#16]
 ldr x1,[sp,#32]
 ldr w2,[sp,#40]
 adrp x8,callbacks
 add x8,x8,:lo12:callbacks
 ldr x8,[x8,#8]
 cbz x8,2f
 blr x8
2:
 ldp x29,x30,[sp]
 add sp,sp,#64
 ret
.global rc6_original_apply
rc6_original_apply:
 cbz w1,3f
 b original_apply_ret
3:
 sub sp,sp,#0x80
 stp x29,x30,[sp,#0x20]
 stp x28,x27,[sp,#0x30]
 b original_apply_tail
.global rc6_rating
rc6_rating:
 sub sp,sp,#48
 stp x29,x30,[sp]
 mov x29,sp
 stp x0,x1,[sp,#16]
 adrp x8,callbacks
 add x8,x8,:lo12:callbacks
 ldr x8,[x8,#16]
 cbz x8,4f
 blr x8
 cbnz w0,5f
4:
 ldp x0,x1,[sp,#16]
 ldp x29,x30,[sp]
 add sp,sp,#48
 b rc6_original_rating
5:
 ldp x0,x1,[sp,#16]
 ldp x29,x30,[sp]
 add sp,sp,#48
 ret
.global rc6_original_rating
rc6_original_rating:
 stp d15,d14,[sp,#-0xa0]!
 stp d13,d12,[sp,#0x10]
 stp d11,d10,[sp,#0x20]
 stp d9,d8,[sp,#0x30]
 b original_rating_tail
