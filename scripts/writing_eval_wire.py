# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2,<3"]
# ///
# How to run: python3 -m pytest -q scripts/test_writing_eval_relative_read.py scripts/test_writing_eval_reference_handles.py
"""Normalized evaluation wire models, separate from validation policy."""
from typing import ClassVar, Literal, assert_never
from pydantic import BaseModel, ConfigDict, Field

class ContentBlock(BaseModel):
    type: str
    text: str | None = None


class WireMessage(BaseModel):
    role: str
    stopReason: str | None = None
    content: tuple[ContentBlock, ...] | str | None = ()

    def successful_text(self) -> bool:
        if self.role != "assistant" or self.stopReason != "stop":
            return False
        match self.content:
            case str() as text:
                return bool(text.strip())
            case tuple() as blocks:
                return any(b.type == "text" and b.text is not None and bool(b.text.strip()) for b in blocks)
            case remaining:
                if remaining is None:
                    return False
                assert_never(remaining)


class ReadArgs(BaseModel):
    path: str | None = None
    relative_to: str | None = None
    reference_id: str | None = None


class WireEvent(BaseModel):
    type: str
    toolCallId: str | None = None
    toolName: str | None = None
    args: ReadArgs | None = None
    isError: bool = False
    message: WireMessage | None = None
    aborted: bool = False
    path: str | None = None
    offset: int | None = Field(default=None, ge=1)
    returned_lines: int | None = Field(default=None, ge=0)
    content_sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")


class RunReceipt(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")
    run_id: str
    status: Literal["completed", "INCONCLUSIVE"]
    input_sha256: str
    source_before: str
    source_after: str
    trace: tuple[WireEvent, ...] = ()
    reason: str | None = None
