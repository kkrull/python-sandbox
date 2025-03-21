% SODE(1) Version 0.0.2 | BRODE SODE
% Kyle Krull
% March 2025

# NAME

**fs-find** - Find source files

# DESCRIPTION

**fs-find** helps you search for source files among several Git repositories
that you have cloned.

This is useful when you don't know ahead of time which specific repositories to
look in.  It helps you filter out non-source files that also exist in those
directories, so you can find what you are looking for.

# EXAMPLE

## JavaScript module index

_...or was that TypeScript?_

I'm looking for recently-edited index files form some sort of JavaScript (or
TypeScript) project that may or may not be using JSX/TSX.  I can't remember
which repository I was working in, last time I did this, and I would like to
find an example from my recent work.

There are 28 repositories in my organization alone, so I can't `git grep`
through each of them.

I remember part of the filename (`index`), but that happens to be a
commonly-used filename.  I can't quite remember the extension, and I'm not sure
if a glob pattern that works in the shell (e.g. `index.[jt]s[x?]`) will also
work in `find`.

### Use `find` to search for files in lots of places

I can run `find` over 1 or more organizations using readily available commands:

```shell
# git/kkrull.github.com
find . -type f -name 'index*'
```

What I'm looking for are files like these:

```shell
# Files I muse have worked on recently (3)
./node-sandbox/conway-js/src/index.js
./node-sandbox/conway-ts/src/index.ts
./node-sandbox/node-executable/greeter-lib/index.js
```

### Filter out false positives

There are also a lot of false positives.  The most distracting ones are the
non-source files that match this same pattern:

```shell
# git internals (29)
./bambam/.git/index

# files downloaded by package managers (1450)
./bambam/node\_modules/@colors/colors/index.d.ts
```

There are also a few false negatives from real source files that match my
imperfect search pattern. There are a few, but it is not quite as distracting:

```shell
# wrong file extension (15)
./blog-apprenticeship/index.md # (2)
./java-sandbox/hibernate/hibernate.webapp/src/main/webapp/index.jsp # (2)
./java-sandbox/jetty/src/main/webapp/index.html # (11)
```

I can refine my command by filtering out false positives, but it's a somewhat
clunky process:

```shell
find . -type f -name 'index*' | sort | grep -v '.git' | grep -v node_modules
```

or better yet:

```shell
# ~/git
find bitovi.github.com kkrull.github.com -type f \
  -name 'index[.][jt]s' -or -name 'index[.][jt]sx' \
  | grep -v '[.]git/' \
  | grep -v 'node\_modules'
```

### A new tool could help

What I would really like to do, is something like this:

```shell
# ~/git
$ sode fs find 'index*' kkrull.github.com bitovi.github.com
Pattern matches 99 files
bitovi.github.com/enterprise-grade-micro-frontends/packages/catalog/src/index.tsx
bitovi.github.com/enterprise-grade-micro-frontends/packages/catalog/src/scenes/CatalogItem/index.ts
...
kkrull.github.com/node-sandbox/conway-js/src/index.js
kkrull.github.com/node-sandbox/conway-ts/src/index.ts
kkrull.github.com/node-sandbox/node-executable/greeter-lib/index.js
```

# SEE ALSO

[*sode(1)*](./sode.1.md),
