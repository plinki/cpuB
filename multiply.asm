
MOV ra, 0   
MOV rb, 5 
MOV rc, 3 
MOV rd, 1
MOV re, 1   

ADD rc, re

MOV rg, loop 

loop:
    ADD ra, rb  
    ADD rd, re   
    JNE rd, rc  
    STORE ra

    ; The result is now in R1
