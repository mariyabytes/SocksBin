SocksBin
=====

Command line pastebin for sharing files and command outputs.

# How to use

### Requirements
To use this, you'll need a tool called **netcat**. Try typing 'nc' or 'netcat' into the terminal, you probably have it already !

_________
### Client Side

* Self-Explanatory examples using the public server


```
echo "Hello World !" | nc magnum.wtf 6969
```

```
cat "script.sh" | nc magnum.wtf 6969
```

* In case you started the server on localhost


```
df | nc localhost 9999
```

____

You will receive a url to the text-only paste as a response to the above commands. e.g.

```
https://socksbin.magnum.wtf/33fdd867
```

This has a built-in Pygment-based beautifier. add "_color" to the end of the received url, to get a beautified paste.

```
https://socksbin.magnum.wtf/33fdd867_color
```

<sup>In case your text isn't beautified, include the *shebang* `#!` which is the first two bytes of an executable</sup>

<sup> e.g. the first line should be `#! /usr/bin/env python` for proper python formatting</sup>

-------------------------------------------------------------------------------

## Cool stuff

Make this much easier to use by adding an alias to your rc file. For example:

-------------------------------------------------------------------------------

### `skb` alias

__Linux (Bash):__

```
echo 'alias skb="nc magnum.wtf 6969"' >> .bashrc
```


__macOS:__

```
echo 'alias skb="nc magnum.wtf 9999"' >> .bash_profile
```

-------------------------------------------------------------------------------

### Copy output to clipboard

__Linux (Bash):__
```
echo 'alias tbc="netcat termbin.com 9999 | xclip -selection c"' >> .bashrc
```

```
echo less typing now! | tbc
```

__macOS:__

```
echo 'alias tbc="nc termbin.com 9999 | pbcopy"' >> .bash_profile
```

```
echo less typing now! | tbc
```

__Remember__ to reload the shell with `source ~/.bashrc` or `source ~/.bash_profile` after adding any of provided above!

-------------------------------------------------------------------------------



