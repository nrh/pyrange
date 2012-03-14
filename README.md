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

* Give me a list of all my hosts that serve pgsql
`GET /apps/pgsql`
`{"members": ["db1.phoenix.foo","db2.phoenix.foo","db1.london.foo",...]}`

* Give me a list of all my hosts that are in london
`GET /sites/london`
`{"members": ["db1.london.foo","web1.london.foo","gopher3.london.foo",...]}`

* Give me a list of all my pgsql hosts that are in london
`GET /range/@apps.pgsql,&@sites.london` (url-decoded for readability)
`{"members": ["db1.london.foo"]}`

* Create a special role for just london pgsql hosts
`POST /apps/pgsql-london {"definition":["@apps.pgsqlg,&@sites.london"]}`

* Now give me a list of all my pgsql hosts that are in london
`GET /apps/pgsql-london`
`{"members": ["db1.london.foo"]}`

* Add a new database host in london
`POST /apps/pgsql {"append-definition":["db2.london.foo"]}`

* Now give me a list of all my pgsql hosts that are in london
`GET /apps/pgsql-london`
`{"members": ["db1.london.foo"]}`

For more information, see the [wiki](https://github.com/nrh/pyrange/wiki)

