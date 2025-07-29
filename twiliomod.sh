#!/data/data/com.termux/files/usr/bin/bash

# Usage: ./twilio_check.sh <env-file> <to-phone-number>
# Example: ./twilio_check.sh creds.env +919876543210

if [ $# -ne 2 ]; then
  echo "Usage: $0 <env-file> <to-phone-number>"
  exit 1
fi

ENV_FILE="$1"
TO="$2"

# Extract Twilio creds from .env
SID=$(grep -E '^TWILIO_SID=' "$ENV_FILE" | cut -d '=' -f2)
TOKEN=$(grep -E '^TWILIO_TOKEN=' "$ENV_FILE" | cut -d '=' -f2)
FROM=$(grep -E '^TWILIO_FROM=' "$ENV_FILE" | cut -d '=' -f2)

if [ -z "$SID" ] || [ -z "$TOKEN" ] || [ -z "$FROM" ]; then
  echo "❌ Missing Twilio credentials in $ENV_FILE"
  exit 1
fi

echo "🚀 Testing Twilio SMS API..."
RESPONSE=$(curl -s -X POST "https://api.twilio.com/2010-04-01/Accounts/$SID/Messages.json" \
  --user "$SID:$TOKEN" \
  --data-urlencode "To=$TO" \
  --data-urlencode "From=$FROM" \
  --data-urlencode "Body=🧠 Termux Twilio Test SMS via LIAAFYO" )

echo "$RESPONSE" | grep -q '"status":' && echo "✅ SMS sent or queued." || echo "❌ Failed to send SMS."
echo
echo "📨 Full response:"
echo "$RESPONSE"
