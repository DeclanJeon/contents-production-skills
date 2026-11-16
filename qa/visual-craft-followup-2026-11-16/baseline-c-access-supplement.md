# Baseline C — supplemental file-access evidence

The original receipt collector enumerated only tool name `read`; it was not a complete file-access inventory. Parent checked the raw baseline-C session after the final reviewer flagged a missing read.

- Session: the session path recorded for baseline C in application-read-receipts.json.
- Tool: bash.
- Call ID: `call_a580958bffb84f2ea105fceff61d5107|fc_0fc80963f98a7253016afaf87069ac87d09ac0a84b2d0e6d1d`.
- Command: `sed -n '28,37p;48,60p' video-production-assets/references/performance-and-style-recipes.md`.
- Matching toolResult: isError=false,durationMs21,timestamp1794832497105.
- Returned text actually contains `## 진행 중 과제: 주의가 바뀐 뒤에도 몸과 물체는 이어진다` and `## 협업: 여러 명의 동작보다 서로 필요한 역할`,with their complete selected paragraphs and common evidence limits.

Thus baseline C did access both cited sections. Its self-report was not an unsupported access claim. The final review's Minor1 is rejected on this concrete contrary evidence,not silently erased: final-review.md remains unchanged. Baseline/loaded drafts and their hashes remain unchanged. Tool-choice deviation (bash/sed instead of read) is separate from whether access happened and creates no new product rule.
