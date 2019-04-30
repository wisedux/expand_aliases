# expand_aliases
Recursively expand a mail `/etc/aliases` file so there's no nesting.

Sometimes you want to know which aliases a given email address is a member 
of.  You can do this by hand, but it is tedious if you have nested aliases. 
This script takes a regular `/etc/aliases` file and resolves all aliases 
down to their leaves so you can `grep` for an address to see what they're a
member of.

This doesn't explicitly support all alias features, such as pipes.  If you 
have any leaves that aren't email addresses or paths, it will call it 
"WEIRD" but will probably work anyway.

This script does not attempt to use SMTP `expn` or `vrfy` commands.  If you 
want to try that, use the [expn](https://linux.die.net/man/1/expn) command. 
Beware, it can be noisy for the postmaster.

## Usage

```
$ ./expand_aliases.py -h
usage: expand_aliases.py [-h] [-c] aliases

positional arguments:
  aliases      aliases file

optional arguments:
  -h, --help   show this help message and exit
  -c, --count  show counts
```

### Example

To expand an aliases file, just specify the input as an argument.
```
$ ./expand_aliases.py aliases_example
eggheads: bob@example.com,otis@example.com,sandra@example.com,kent@example.com,pat@example.com
hr: otis@example.com,sandra@example.com
sales: kent@example.com,pat@example.com
devs: sally@example.com,alice@example.com,bill@contoso.com
admins: todd@example.com,susan@example.com
nerds: susan@example.com,alice@example.com,sally@example.com,bob@example.com,todd@example.com,bill@contoso.com
staff: susan@example.com,bob@example.com,otis@example.com,sally@example.com,sandra@example.com,alice@example.com,pat@example.com,todd@example.com,kent@example.com,bill@contoso.com
```

If you want to know how many [local] members each alias has, specify 
the `-c` flag:
```
$ ./expand_aliases.py -c aliases_example
5 eggheads: bob@example.com,otis@example.com,sandra@example.com,kent@example.com,pat@example.com
2 hr: otis@example.com,sandra@example.com
2 sales: kent@example.com,pat@example.com
3 devs: sally@example.com,alice@example.com,bill@contoso.com
2 admins: todd@example.com,susan@example.com
6 nerds: susan@example.com,alice@example.com,sally@example.com,bob@example.com,todd@example.com,bill@contoso.com
10 staff: susan@example.com,bob@example.com,otis@example.com,sally@example.com,sandra@example.com,alice@example.com,pat@example.com,todd@example.com,kent@example.com,bill@contoso.com
```
