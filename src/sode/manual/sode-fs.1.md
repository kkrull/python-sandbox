% SODE(1) Version 0.0.1 | BRODE SODE
% Kyle Krull
% March 2025

# NAME

**sode fs** - Hack the local file system

# SYNOPSIS

**sode fs** \[**\-\-help**\]  
**sode fs** *sub-command* \[*args* …\]

# DESCRIPTION

**sode fs** runs the given *sub-command* with any *args*, to do something with
the local filesystem.

# OPTIONS

  - **\-\-help**
    Show help

# SUB-COMMANDS

  - [**find**](./fs-find.1.md)
    Find files in a filesystem

# EXIT STATUS

  - 0
    Success

  - 1+
    Invalid command or command failure

# SEE ALSO

[*sode(1)*](./sode.1.md)
[*sode-fs-find(1)*](./sode-fs-find.1.md),

[*sode(7)*](./sode.7.md)
