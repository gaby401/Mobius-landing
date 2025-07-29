#!/bin/bash
echo "[+] Scanning files for juicy secrets..."

grep -rE --color=always \
  -e "0x[a-fA-F0-9]{64}" \
  -e "eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+" \
  -e "(?i)api[_-]?key.{0,10}['\"][A-Za-z0-9_\-]{16,64}" \
  -e "(?i)secret.{0,10}['\"][A-Za-z0-9_\-]{16,64}" \
  -e "\b(?:[a-z]{3,10}\s){11,23}[a-z]{3,10}\b" \
  -e "\[\s*(?:\d{1,3},\s*){10,}\d{1,3}\s*\]" \
  node_modules_dump/ 2>/dev/null
