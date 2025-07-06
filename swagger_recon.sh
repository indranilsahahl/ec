#!/bin/bash

# Dependencies check
command -v jq >/dev/null 2>&1 || { echo >&2 "jq is required but not installed. Installing..."; sudo apt install -y jq; }
command -v http >/dev/null 2>&1 || { echo >&2 "httpie not found. Installing..."; sudo apt install -y httpie; }

# Target and output
TARGET="https://petstore.swagger.io/v2/swagger.json"
OUTPUT_FILE="swagger_api_recon.txt"

echo "[*] Fetching Swagger JSON from $TARGET..."
curl -s "$TARGET" -o swagger.json || { echo "[-] Failed to fetch API spec"; exit 1; }

echo "[+] Saving reconnaissance results to $OUTPUT_FILE"
echo "==== API Reconnaissance Report ====" > $OUTPUT_FILE
echo "Target: $TARGET" >> $OUTPUT_FILE
echo "" >> $OUTPUT_FILE

# 1. Extract API Info
echo "==== [1] API Information ====" >> $OUTPUT_FILE
jq '.info' swagger.json >> $OUTPUT_FILE
echo "" >> $OUTPUT_FILE

# 2. Extract API Host & BasePath
echo "==== [2] Host & Base Path ====" >> $OUTPUT_FILE
jq -r '.host, .basePath' swagger.json >> $OUTPUT_FILE
echo "" >> $OUTPUT_FILE

# 3. Extract All Paths and Methods
echo "==== [3] API Routes & Methods ====" >> $OUTPUT_FILE
jq -r '.paths | to_entries[] | "\(.key) -> \(.value | to_entries[] | .key)"' swagger.json >> $OUTPUT_FILE
echo "" >> $OUTPUT_FILE

# 4. Extract Route Summaries
echo "==== [4] Endpoint Summary ====" >> $OUTPUT_FILE
jq -r '.paths | to_entries[] | 
      .key as $path | 
      .value | to_entries[] | 
      "[$path] [\(.key | ascii_upcase)] Summary: \(.value.summary)"' swagger.json >> $OUTPUT_FILE
echo "" >> $OUTPUT_FILE

# 5. Extract Parameters & Response Info
echo "==== [5] Endpoint Parameters & Response Codes ====" >> $OUTPUT_FILE
jq -r '
  .paths | to_entries[] |
  .key as $path |
  .value | to_entries[] |
  .key as $method |
  .value |
  "[$method] $path\n  Parameters:" +
  (if .parameters then
    (.parameters[] | "    - \(.name) (\(.in)) [required=\(.required)]")
   else
    "\n    - None"
   end) +
  "\n  Responses:" +
  (.responses | to_entries[] | "    - Code: \(.key), Description: \(.value.description)")
' swagger.json >> $OUTPUT_FILE
echo "" >> $OUTPUT_FILE

# 6. Identify Technologies (based on headers)
echo "==== [6] Server & Technology Fingerprinting ====" >> $OUTPUT_FILE
http --headers GET https://petstore.swagger.io/v2/pet 2>/dev/null | \
grep -iE "Server:|X-Powered-By:" >> $OUTPUT_FILE || \
echo "Could not detect technology stack." >> $OUTPUT_FILE
echo "" >> $OUTPUT_FILE

# Cleanup
rm -f swagger.json

echo "[+] Recon complete. Output saved to $OUTPUT_FILE"
