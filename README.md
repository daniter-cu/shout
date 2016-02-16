# Shout
Shout is a decentralized chat client that using broadcast messaging.

## Install instructions

#### Install urwid
```
apt-get install python-urwid
```
Or follow these instructions.
```
$ git clone git://github.com/wardi/urwid.git
$ cd urwid
$ gcc-4.2 -fno-strict-aliasing -fno-common -dynamic -DNDEBUG -g -fwrapv -Os -Wall -Wstrict-prototypes -DENABLE_DTRACE -arch i386 -arch x86_64 -pipe -I/System/Library/Frameworks/Python.framework/Versions/2.6/include/python2.6 -c source/str_util.c -o build/temp.macosx-10.6-universal-2.6/source/str_util.o
$ python setup.py build
$ python setup.py install
```

#### Run SHOUT
```
$ git clone https://github.com/daniter-cu/shout.git
$ python shout.py
```

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

