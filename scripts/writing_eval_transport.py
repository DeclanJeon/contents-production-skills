# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2,<3"]
# ///
# How to run: python3 -m pytest -q scripts/test_writing_eval_rpc.py
"""Bounded LF-framed RPC pipes; no model selection or rubric decisions."""
from __future__ import annotations

from contextlib import suppress
from dataclasses import dataclass
import os
from pathlib import Path
import selectors
import signal
import subprocess
import time
from typing import BinaryIO, ClassVar, IO, Literal

from pydantic import BaseModel, ConfigDict, Field


class RpcProfile(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")
    executable: str = Field(min_length=1)
    provider: str = Field(min_length=1)
    model: str = Field(min_length=1)
    thinking: Literal["off", "minimal", "low", "medium", "high", "xhigh", "max"]
    timeout_seconds: float = Field(gt=0, allow_inf_nan=False)


@dataclass(frozen=True, slots=True)
class RpcWorkspace:
    root: Path
    output: Path


class RpcCommand(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")
    id: str
    type: Literal["set_auto_retry", "set_auto_compaction", "prompt"]
    enabled: bool | None = None
    message: str | None = None


class ResponseData(BaseModel):
    disposition: str | None = None


class RpcEvent(BaseModel):
    """Parse protocol control fields; other progress data stays in raw logs."""
    type: str
    id: str | None = None
    command: str | None = None
    success: bool | None = None
    aborted: bool = False
    error: str | None = None
    data: ResponseData | None = None


class RpcProtocolError(RuntimeError):
    reason: str

    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)


class RpcPipe:
    """Mutable byte buffer owned by one child and one case conversation."""

    process: subprocess.Popen[bytes]
    stdout: IO[bytes]
    stdin: IO[bytes]
    timeout: float
    pending: bytes

    def __init__(self, process: subprocess.Popen[bytes], timeout: float) -> None:
        if process.stdout is None or process.stdin is None:
            raise RpcProtocolError("RPC requires stdin/stdout pipes")
        self.process = process
        self.stdout = process.stdout
        self.stdin = process.stdin
        self.timeout = timeout
        self.pending = b""

    def exchange(self, command: RpcCommand, log: BinaryIO) -> bytes:
        payload = command.model_dump_json(exclude_none=True).encode() + b"\n"
        _ = self.stdin.write(payload)
        self.stdin.flush()
        deadline = time.monotonic() + self.timeout
        acknowledged = False
        settled = False
        lines: list[bytes] = []
        with selectors.DefaultSelector() as selector:
            _ = selector.register(self.stdout, selectors.EVENT_READ)
            while not (acknowledged and (settled or command.type != "prompt")):
                while b"\n" not in self.pending:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0 or not selector.select(remaining):
                        raise RpcProtocolError("RPC deadline exceeded before settled")
                    chunk = os.read(self.stdout.fileno(), 65536)
                    if not chunk:
                        raise RpcProtocolError("RPC peer exited before completion")
                    self.pending += chunk
                    _ = log.write(chunk)
                    log.flush()
                raw, self.pending = self.pending.split(b"\n", 1)
                if not raw.strip():
                    continue
                lines.append(raw + b"\n")
                event = RpcEvent.model_validate_json(raw)
                # Open-world progress events are preserved, not exhaustively enumerated.
                match event.type:  # noqa: MATCH_OK — open protocol preserves unknown progress events
                    case "response":
                        if event.id != command.id:
                            continue
                        if event.command != command.type or event.success is not True:
                            raise RpcProtocolError(event.error or "RPC command rejected")
                        if command.type == "prompt" and (
                            event.data is None or event.data.disposition != "started"
                        ):
                            raise RpcProtocolError("Prompt handled or queued; no attributable run")
                        acknowledged = True
                    case "agent_settled":
                        if event.aborted:
                            raise RpcProtocolError("RPC run aborted")
                        settled = True
                    case _:
                        continue
        return b"".join(lines)


def shutdown(process: subprocess.Popen[bytes]) -> None:
    """RPC EOF requests graceful shutdown; deadlines reap the process group."""
    if process.stdin is not None and not process.stdin.closed:
        # A peer may disconnect while EOF is requested; bounded wait still reaps it.
        with suppress(BrokenPipeError):
            process.stdin.close()
    try:
        _ = process.wait(timeout=0.3)
    except subprocess.TimeoutExpired:
        # The child may finish between wait's timeout and the termination signal.
        with suppress(ProcessLookupError):
            os.killpg(process.pid, signal.SIGTERM)
        try:
            _ = process.wait(timeout=0.5)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            _ = process.wait(timeout=0.5)
