pyrange: simple API for storing lists of hosts
----------------------------------------------

A clean, python+bottle+gevent-based reimplementation of the excellent
range utilities developed at Yahoo: https://github.com/ytoolshed/range/

When you manage a large amount of hosts, it is important to be able to:
* address groups of hosts not by lists of individual names, but based on
  function
* easily share, modify and manipulate those groups
* apply your own semantics

pyrange by example
------------------

### Give me a list of all my hosts that serve pgsql

    > GET /apps/pgsql

    < 200 OK
    < {"members": ["db1.phoenix.foo","db2.phoenix.foo","db1.london.foo",...]}

### Give me a list of all my hosts that are in london

    > GET /sites/london

    < 200 OK
    < {"members": ["db1.london.foo","web1.london.foo","gopher3.london.foo",...]}

### Give me a list of all my pgsql hosts that are in london

    > POST /range/
    > {"members":["@apps.pgsql,&@sites.london"]}

    < 200 OK
    < {"members": ["db1.london.foo"]}

### Create a special role for just london pgsql hosts

    > PUT /apps/pgsql-london
    > {"definition":["@apps.pgsqlg,&@sites.london"]}`

    < 201 OK Created /apps/pgsql-london

### Now give me a list of all my pgsql hosts that are in london

    > GET /apps/pgsql-london

    < 200 OK
    < {"members": ["db1.london.foo"]}

## Add a new database host in london

    > PUT /apps/pgsql/definition
    > {"append":["db2.london.foo"]}`

    < 200 OK Appended /apps/pgsql/definition

### Now give me a list of all my pgsql hosts that are in london

    > GET /apps/pgsql-london

    < 200 OK
    < {"members": ["db1.london.foo"]}

For more information, see the [wiki](https://github.com/nrh/pyrange/wiki)

