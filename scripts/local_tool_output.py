"""Capture output from the two local CLI tools used by the import and privacy checks."""

import asyncio
import shutil
from pathlib import Path


def read_output(command: list[str]) -> bytes:
    name, *arguments = command
    if name not in {"git", "pdftotext"}:
        raise ValueError("Unsupported executable")
    executable = shutil.which(name)
    if executable is None or not Path(executable).is_absolute():
        raise RuntimeError(f"Cannot resolve {name} to an installed executable")

    async def capture() -> bytes:
        process = await asyncio.create_subprocess_exec(
            executable, *arguments, stdout=asyncio.subprocess.PIPE
        )
        stdout, _ = await process.communicate()
        if process.returncode:
            raise RuntimeError(f"{name} failed with exit status {process.returncode}")
        return stdout

    return asyncio.run(capture())
