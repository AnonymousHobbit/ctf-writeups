en_flag = "DJ?EyPMRU_qFcpc0.0/{"
flag = ""
for i in range(len(en_flag)):
    flag+=chr(ord(en_flag[i])+2)

print(f"[+] Flag: {flag}")
