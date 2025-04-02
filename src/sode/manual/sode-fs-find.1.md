% SODE(1) Version 0.0.1 | BRODE SODE
% Kyle Krull
% March 2025

# NAME

**sode fs find** - Find source files

# SYNOPSIS

**sode fs find** \[**\-\-help**\]  
**sode fs find** \[**\-\-exclude**\] *glob* **\-\-glob** *glob*
\[\-\-\] \[*path* …\]

# DESCRIPTION

List filenames matching any *glob*-but not an excluded pattern-in any *path*.
Glob patterns allow `**` for recursive matching.

# OPTIONS

  - **\-\-exclude**
    path pattern(s) to exclude (repeatable)

  - **\-\-glob**
    path pattern(s) to match (repeatable)

  - **\-\-help**
    Show help

# EXIT STATUS

  - 0
    Success

  - 1+
    Invalid command or command failure

# EXAMPLE

## Look up Makefiles in local repositories

    sode fs find --glob '**/Makefile' ~/git

# SEE ALSO

[*sode(1)*](./sode.1.md), [*sode-fs(1)*](./sode-fs.1.md)

[*sode(7)*](./sode.7.md)
