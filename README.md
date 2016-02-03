# Shout
Shout is a decentralized chat client that using broadcast messaging.

## Actions

```
{
    "msg": "Hello, World", # Message sent to the chat room
    "hello": "", # Ping to discover if a room exists.
    "rename": "Hotel California", # Rename the chat room.
    "name": "Batman.", # Change your name.
    "help": "", # Display a list of commands.
}
```

If no action word is specified, it defaults to msg.
Automatically sent when the program is first started. This step might not be necessary.

