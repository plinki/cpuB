; X-Y limit
MOV re, 64

; Store 1 in ra
MOV ra, 1

; Counter X and counter Y
MOV rb, 0
MOV rc, 0

; Global counter
MOV rd, 0

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;Set X and Y VRAM locations to 0
; Set VRAM Register (rf) to 0 (rd holds 0) for X
MOV rh, 0

MOV2 rf, rd
STORE rf

;Same for Y
MOV rh, 1
STORE rf

;; 11 instructions
; Move to first pixel vram location (2)
MOV rh, 2

draw:
    ; Add one to global counter
    ADD rd, ra

    ADD rb, ra
    MOV rh, 0

    MOV rf, 0
    MOV2 rf, rb
    SUB rf, ra
    STORE rf

    ; Here we need to go to next pixel
    ; What I did was set rg to 0, added X counter to rg,
    ; And added 1 to rg,

    ; Now trying with rd instead of rb as it's the global counter
    MOV rg, 0
    MOV2 rg, rd
    ADD rg, ra

    ; So here we basically move X Counter+1 into MAR
    MOV2 rh, rg
    
    ; move draw location to jump register 
    MOV rg, draw
    JLT rb, re
    

; Go to Y Vram location
MOV rh, 1

; Lets add 1 to Y Counter and store it in VRAM
MOV rf, 0
ADD rc, ra
MOV2 rf, rc
STORE rf

MOV rb, 0

JLT rc, re
