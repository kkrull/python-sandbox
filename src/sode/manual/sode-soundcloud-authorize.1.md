% SODE(1) Version 0.0.1 | BRODE SODE
% Kyle Krull
% March 2025

# NAME

**sode soundcloud authorize** - Authorize with SoundCloud

# SYNOPSIS

**sode soundcloud authorize** \[**\-\-help**\]  
**sode soundcloud authorize**

# DESCRIPTION

**sode soundcloud authorize** authorizes use of the SoundCloud API, for your
account.

This is a necessary first step to using the API.

# OPTIONS

  - **\-\-help**
    Show help

# ENVIRONMENT VARIABLES

See [*sode-soundcloud(1)*](./sode-soundcloud.1.md).

# EXIT STATUS

  - 0
    Success

  - 1+
    Invalid command or command failure

# EXAMPLE

    CLIENT_ID=client-secret CLIENT_SECRET=client-secret sodesoundcloud authorize

# SEE ALSO

[*sode(1)*](./sode.1.md), [*sode-soundcloud(1)*](./sode-soundcloud.1.md)

[*sode(7)*](./sode.7.md)
