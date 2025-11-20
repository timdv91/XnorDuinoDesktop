#!/bin/bash
# Carport open notifier for Discord
discord_url="xxxxxxxxxxxxxxxxxxxxx"
# Send a basic message:
generate_post_data_open()
{
    cat <<EOF
    {
      "content": "Carport is open!!!",
      "embeds": [{
        "title": "Carport is open!!!",
        "description": "Carport is open!!!"
      }]
    }
EOF
}

generate_post_data_close()
{
    cat <<EOF
    {
      "content": "Carport is closed!!!",
      "embeds": [{
        "title": "Carport is closed!!!",
        "description": "Carport is closed!!!"
      }]
    }
EOF
}

postText_opened()
{
    wget -q \
     --timeout=5 \
     --method=POST \
     --header="Content-Type: application/json" \
     --body-data="$(generate_post_data_open)" \
     "$discord_url" -O /dev/null
}

postText_closed()
{
    wget -q \
     --timeout=5 \
     --method=POST \
     --header="Content-Type: application/json" \
     --body-data="$(generate_post_data_close)" \
     "$discord_url" -O /dev/null
}

if [ "$1" = "true" ]; then
  postText_opened
else
  postText_closed
fi