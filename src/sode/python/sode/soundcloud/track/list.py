from sode.shared.cli import ProgramNamespace, RunState


def list_tracks(args: ProgramNamespace, state: RunState) -> int:
    print(f"Listing tracks...", file=state.stdout)
    return 0
