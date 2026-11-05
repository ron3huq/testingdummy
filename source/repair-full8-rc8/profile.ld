rc8_name = 0x110000; old_profile_continue = 0x1a5ec;
SECTIONS { . = 0x101000; .text : { *(.text*) } /DISCARD/ : { *(.comment*) *(.note*) *(.eh_frame*) } }
