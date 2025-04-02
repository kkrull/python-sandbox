# Code Structure

## Principles

1. Adding a new (sub-)command should not require modifying any other command's code.
2. A separate main package is responsible for creation, wiring, and orchestration.  It is the only
   package that may depend upon-and have code references to-everything else.
3. ~~All code for parsing and running each (sub-)command should be in its own package, to group
   together code that has the same reasons to change (e.g. package by feature).~~

   _Note: Delegating logic to configure argparse to another package is proving to be difficult.  Try
   doing it all from main for now.  Maybe there will be a way to delegate some of that behavior
   later._

## Package dependencies

Packages are structured as follows, to orient dependencies in the necessary manner:

```mermaid
graph TB

subgraph Main
  cli
end

Main --> Commands
subgraph Commands
  direction RL

  cli.fs -.->|as needed| cli.root
  cli.fs.find -.->|as needed| cli.fs
end

Commands --> Libraries
subgraph Libraries
  cli.shared --> argparse
end
```

Arrows represent code references from one package to another.

## Workflow

### 01: main creates parsers

`main` makes a `Parser` for each command and then links them together, so that each parser can reach
child parsers for (sub-)commands.

```mermaid
graph LR

terminal
cli.main
subgraph Commands
  direction TB
  cli.root(cli.root<br/>RootParser)
  cli.fs(cli.fs<br/>FsParser)
  cli.fs.find(cli.fs.find<br/>FindParser)
end

terminal -->|argv| cli.main
cli.main -->|new_parser <br/> add_child__cli.fs| cli.root
cli.main -->|new_parser <br/> add_child__cli.fs.find| cli.fs
cli.main -->|new_parser| cli.fs.find
```

### 02: parse arguments

`main` passes arguments to the root parser, which delegates to child parsers to parse (sub-)command
arguments and decide upon which operation(s) to process.

This results in either a `CliCommand` that performs the indicated operation (valid arguments) or an
error (invalid arguments).  The command has access to all arguments: its own, as well as any
affecting global behavior (e.g. verbose output).

```mermaid
graph RL

cli.main
subgraph Commands
  direction TB
  cli.root(cli.root<br/>RootAction, RootArgs, RootParser)
  cli.fs(cli.fs<br/>FsAction, FsArgs, FsParser)
  cli.fs.find(cli.fs.find<br/>FindAction, FindArgs, FindParser)
end

cli.main -->|RootParser#parse_arguments__argv| Commands
cli.root -->|parse_arguments__argv-globals| cli.fs
cli.fs -->|parse_arguments__argv-fs| cli.fs.find

cli.fs -.->|add_args__fs| cli.root
cli.fs.find -.->|add_args__find| cli.fs

Commands -.->|CliCommand__Args| cli.main
```

### 03: run command and exit

`main` constructs a state in which to run commands, which contains any dependencies (e.g. services
or I/O) the command needs to run.  It uses environment variables and/or arguments to override
default configuration.

It then uses this state to run the `CliCommand`.  The command returns a result that is either
success or an error, and main determines and exits with a suitable status code.

```mermaid
graph RL

terminal
subgraph cli.main
  direction TB
  main.py
  MainState

  main.py -->|MainState::new<br/>MainState#to_run_state| MainState
end

subgraph cli.shared
  direction TB
  CliCommand
  RunState

  CliCommand -.-> RunState
end

subgraph cli.fs.find
  direction TB
  FindCommand
end


terminal -->|argv| cli.main
cli.main -->|RunState::new| cli.shared

cli.main -->|CliCommand#run| cli.shared
cli.fs.find -.->|implements<br/>CliCommand| cli.shared
cli.fs.find -->|RunState#read| cli.shared

cli.shared -.->|Success<br/>Error| cli.main
cli.main -.->|exit status| terminal
```
