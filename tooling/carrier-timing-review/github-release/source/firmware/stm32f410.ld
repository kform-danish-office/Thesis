/* STM32F410CBU6: vectors in sector 0, settings in sector 1, code in sectors 2-4. */
ENTRY(Reset_Handler)
_Min_Heap_Size = 0x400;
_Min_Stack_Size = 0x800;

MEMORY
{
  RAM     (xrw) : ORIGIN = 0x20000000, LENGTH = 32K
  VECTORS (rx)  : ORIGIN = 0x08000000, LENGTH = 16K
  SETTINGS (r)  : ORIGIN = 0x08004000, LENGTH = 16K
  FLASH   (rx)  : ORIGIN = 0x08008000, LENGTH = 96K
}

_estack = ORIGIN(RAM) + LENGTH(RAM);
__settings_start__ = ORIGIN(SETTINGS);
__settings_end__ = ORIGIN(SETTINGS) + LENGTH(SETTINGS);
__app_flash_start__ = ORIGIN(FLASH);

SECTIONS
{
  .isr_vector :
  {
    . = ALIGN(4);
    KEEP(*(.isr_vector))
    . = ALIGN(4);
    __vector_end__ = .;
  } > VECTORS

  .text :
  {
    . = ALIGN(4);
    *(.text .text*)
    *(.glue_7 .glue_7t .eh_frame)
    KEEP(*(.init))
    KEEP(*(.fini))
    . = ALIGN(4);
    _etext = .;
  } > FLASH

  .rodata :
  {
    . = ALIGN(4);
    *(.rodata .rodata*)
    . = ALIGN(4);
  } > FLASH

  .ARM.extab :
  {
    . = ALIGN(4);
    *(.ARM.extab* .gnu.linkonce.armextab.*)
    . = ALIGN(4);
  } > FLASH

  .ARM.exidx :
  {
    . = ALIGN(4);
    __exidx_start = .;
    *(.ARM.exidx*)
    __exidx_end = .;
    . = ALIGN(4);
  } > FLASH

  .preinit_array :
  {
    PROVIDE_HIDDEN(__preinit_array_start = .);
    KEEP(*(.preinit_array*))
    PROVIDE_HIDDEN(__preinit_array_end = .);
  } > FLASH
  .init_array :
  {
    PROVIDE_HIDDEN(__init_array_start = .);
    KEEP(*(SORT(.init_array.*)))
    KEEP(*(.init_array*))
    PROVIDE_HIDDEN(__init_array_end = .);
  } > FLASH
  .fini_array :
  {
    PROVIDE_HIDDEN(__fini_array_start = .);
    KEEP(*(SORT(.fini_array.*)))
    KEEP(*(.fini_array*))
    PROVIDE_HIDDEN(__fini_array_end = .);
  } > FLASH

  _sidata = LOADADDR(.data);
  .data :
  {
    . = ALIGN(4);
    _sdata = .;
    *(.data .data*)
    *(.RamFunc .RamFunc*)
    . = ALIGN(4);
    _edata = .;
  } > RAM AT > FLASH

  .bss (NOLOAD) :
  {
    . = ALIGN(4);
    _sbss = .;
    __bss_start__ = .;
    *(.bss .bss*)
    *(COMMON)
    . = ALIGN(4);
    _ebss = .;
    __bss_end__ = .;
  } > RAM

  ._user_heap_stack (NOLOAD) :
  {
    . = ALIGN(8);
    PROVIDE(end = .);
    PROVIDE(_end = .);
    . = . + _Min_Heap_Size + _Min_Stack_Size;
    . = ALIGN(8);
  } > RAM

  .ARM.attributes 0 : { *(.ARM.attributes) }
}

ASSERT(LD_FLASH_OFFSET == 0, "F410 layout requires vectors at 0x08000000")
ASSERT(__vector_end__ <= ORIGIN(SETTINGS), "Vectors overlap settings")
ASSERT(LOADADDR(.data) + SIZEOF(.data) <= 0x08020000, "F410 flash overflow")
