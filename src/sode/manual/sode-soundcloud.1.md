% SODE(1) Version 0.0.1 | BRODE SODE
% Kyle Krull
% March 2025

# NAME

**sode soundcloud** - Hack SoundCloud

# SYNOPSIS

**sode soundcloud** \[**\-\-help**\]  
**sode soundcloud** *sub-command* \[*args* …\]

# DESCRIPTION

**sode soundcloud** runs the given *sub-command* with any *args*, to do something with SoundCloud.

# OPTIONS

  - **\-\-help**
    Show help

# SUB-COMMANDS

  - [**authorize**](./soundcloud-authorize.1.md)
    Authorize with SoundCloud

# ENVIRONMENT VARIABLES

  - **CLIENT\_ID**
    Client ID for the SoundCloud API

  - **CLIENT\_SECRET**
    Client secret for that SoundCloud API client

# EXIT STATUS

  - 0
    Success

  - 1+
    Invalid command or command failure

# SEE ALSO

[*sode(1)*](./sode.1.md)
[*sode-soundcloud-authorize(1)*](./sode-soundcloud-authorize.1.md),

[*sode(7)*](./sode.7.md)
