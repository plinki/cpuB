; RAM(intro_text_location) - where do we put the string?
%const intro_text_location 1
; newline ASCII
%const newline 10
; Location to store user input
%const user_input_mem 20
%const user_input_mem_limit 5

; Change MAR to intro_text_location and write it in ram
MOV rh, intro_text_location
%asciz intro_text "B Computer"

; Store 1 temporarily
MOV rb, 1
; Store newline temporarily
MOV rc, newline
STORE rc
; Add another one
ADD rh, rb
STORE rc

;;; Write string to TTY
; Go back to the start of the string
; Must move string location to MAR first
; MOV rh, M
MOV rh, intro_text_location
write_to_tty:
    ;; We're adding 2 to string length here
    ; Store 2 temporarily
    MOV rb, 2
    ; Store intro_text length in register
    MOV rc, intro_text
    ; add 2 to intro_text length
    ADD rc, rb
    
    ;; Actual writing portion
    ; Counter
    MOV rd, 0
    ; One
    MOV rf, 1
    
    MOV rg, write_loop
    write_loop:
        ; Output character to TTY
        LOAD rb
        STORE rb
    
        ; Go to next character in memory
        ADD rh, rf
        ; Increase counter
        ADD rd, rf
        ; Jump
        JLT rd, rc


; Store 1
MOV ra, 1
; Store 0
MOV rb, 0
; Make sure re (keyboard register) is 0
MOV re, 0

; Lets go back to RAM 0
MOV rh, 0

MOV rg, wait_user_input
; Reset ra to 0 to avoid annoying read_sel problem
MOV ra, 0
; ------------------------------------------------
; One
MOV rd, 1
; Lets use rc as a counter
MOV rc, 0

; Wait until user input
wait_user_input:
    MOV2 re, re
    JEQ re, rb

; User input is in
user_input_in_register:
    MOV rh, user_input_mem
    ADD rh, rc
    ; STORE re
    STORE re

    ADD rc, rd
    
    MOV rf, user_input_mem_limit
    MOV rg, wrap_around
    JGE rc, rf 

    MOV rg, wait_user_input
    JMP

wrap_around:
    MOV rc, 0
    release_input_memory:
        MOV rh, user_input_mem
        ADD rh, rd

        MOV re, 0
        STORE re

        ADD rc, rd
        MOV rg, release_input_memory
        JLE rc, rf

    MOV rc, 0
    MOV rg, wait_user_input
    JMP


; increment_input_counter:
;     ADD rc, rd
;     MOV rg, wait_user_input
;     MOV ra, 0
;     JMP

