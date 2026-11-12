// Controlled T09 fixture. The default path never starts a model or imports its SDK.
import * as fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';

export const INITIAL = 'B01: 처음 문장입니다.\nB02: 루마를 봅니다.\nB03: 끝 문장입니다.\n';
export const INJECTED = 'B01: 사용자 수정 문장입니다.\nB02: 루마를 봅니다.\nB03: 끝 문장입니다.\n';
export const EXPECTED = 'B01: 사용자 수정 문장입니다.\nB02: 옷의 전체 윤곽을 봅니다.\nB03: 끝 문장입니다.\n';
const OWNER = 'video-production-assets/references/03-screenplay.md';
const PREFIX = '이번 작업은 영상 기획/원고 텍스트만입니다. 허용된 임시 fixture의 원고만 수정하고 생성·업로드·게시·외부 변경은 하지 마세요. 제공 자료는 평가용 가정이며 실제 자산을 검사했다고 말하지 마세요.';
const PROMPT = PREFIX + '\n\n허용된 fixture/draft.md에서 B02만 ‘옷의 전체 윤곽을 봅니다.’로 고치세요. 다른 줄은 그대로 두고 저장 직전에 다시 읽어 사용자 수정을 보존하세요.';
const hash = text => createHash('sha256').update(text).digest('hex');
const inside = (root, target) => target === root || target.startsWith(root + path.sep);
const resultText = text => ({ content: [{ type: 'text', text }], details: {} });

export function resolveFixturePath(root, requested) {
  if (typeof requested !== 'string') throw new Error('Invalid fixture path');
  const base = fs.realpathSync(root);
  const relative = requested.startsWith('fixture/') ? requested.slice(8) : requested;
  const target = path.resolve(base, relative);
  if (target !== path.join(base, 'draft.md')) throw new Error('Only fixture/draft.md is writable');
  if (fs.lstatSync(target).isSymbolicLink() || fs.realpathSync(target) !== target) {
    throw new Error('Fixture symlink path refused');
  }
  return target;
}

function validateConfig(config) {
  for (const field of ['snapshotRoot', 'fixtureRoot', 'outputRoot', 'piPackage', 'provider', 'model', 'thinking']) {
    if (typeof config[field] !== 'string' || !config[field].trim()) throw new Error(`Missing ${field}`);
  }
  if (!Number.isFinite(config.timeoutMs) || config.timeoutMs <= 0) throw new Error('Invalid deadline');
  const source = fs.realpathSync(config.snapshotRoot);
  const fixture = fs.realpathSync(config.fixtureRoot);
  const output = path.resolve(config.outputRoot);
  if (inside(source, fixture) || inside(source, output) || inside(fixture, output)
      || inside(output, source) || inside(output, fixture)) throw new Error('Fixture/source/evidence roots must be disjoint');
}

export async function runFixtureCase(config, sessionFactory) {
  validateConfig(config);
  const source = fs.realpathSync(config.snapshotRoot);
  const draft = resolveFixturePath(config.fixtureRoot, 'fixture/draft.md');
  if (fs.readFileSync(draft, 'utf8') !== INITIAL) throw new Error('Unexpected initial fixture; refusing overwrite');
  fs.mkdirSync(config.outputRoot, { recursive: false });
  const eventsPath = path.join(config.outputRoot, 'events.jsonl');
  fs.writeFileSync(eventsPath, '', { flag: 'wx' });
  const emit = event => fs.appendFileSync(eventsPath, JSON.stringify(event) + '\n');
  const pendingReads = new Map();
  let injected = false;
  let reread = false;
  let ownerRead = false;
  let active = true;
  let settled = false;
  let aborted = false;
  let finalMessage = false;
  const ensureActive = () => { if (!active) throw new Error('Fixture run closed'); };
  const write = (requested, text) => {
    ensureActive();
    const target = resolveFixturePath(config.fixtureRoot, requested);
    if (!injected || !reread) throw new Error('Initial-read end event and post-insertion re-read required');
    fs.writeFileSync(target, text, { flag: 'r+' });
    fs.truncateSync(target, Buffer.byteLength(text));
    emit({ type: 'fixture_written', sha256: hash(text) });
    return resultText('Updated fixture/draft.md');
  };
  const tools = [
    { name: 'read', description: 'Read a package Markdown file or fixture/draft.md.', async execute(id, args) {
      ensureActive();
      let target;
      if (args.path === 'fixture/draft.md' || args.path === draft) {
        target = resolveFixturePath(config.fixtureRoot, args.path);
      } else {
        target = fs.realpathSync(path.resolve(source, args.path));
        const parts = path.relative(source, target).split(path.sep);
        if (!inside(source, target) || parts.some(p => p.startsWith('.') || ['qa', 'tests', 'support'].includes(p))
            || !target.endsWith('.md')) throw new Error('Read outside package Markdown refused');
      }
      const contents = fs.readFileSync(target, 'utf8');
      const offset = args.offset ?? 1;
      const limit = args.limit ?? contents.split('\n').length;
      if (!Number.isInteger(offset) || offset < 1 || !Number.isInteger(limit) || limit < 1) throw new Error('Invalid read range');
      const text = contents.split('\n').slice(offset - 1, offset - 1 + limit).join('\n');
      pendingReads.set(id, { target, text });
      emit({ type: 'controlled_read', toolCallId: id, path: target, sha256: hash(text) });
      return resultText(text);
    } },
    { name: 'edit', description: 'Replace one unique exact text in fixture/draft.md.', async execute(id, args) {
      ensureActive();
      const target = resolveFixturePath(config.fixtureRoot, args.path);
      const current = fs.readFileSync(target, 'utf8');
      if (typeof args.oldText !== 'string' || !args.oldText || typeof args.newText !== 'string'
          || current.split(args.oldText).length !== 2) throw new Error('Edit text must match exactly once');
      return write(args.path, current.replace(args.oldText, args.newText));
    } },
    { name: 'write', description: 'Write only fixture/draft.md after re-reading it.', async execute(id, args) {
      if (typeof args.content !== 'string') throw new Error('Write content must be text');
      return write(args.path, args.content);
    } },
  ];
  const onEvent = event => {
    if (!active) return;
    emit(event);
    if (event.type === 'tool_execution_end' && event.toolName === 'read' && !event.isError) {
      const read = pendingReads.get(event.toolCallId);
      pendingReads.delete(event.toolCallId);
      if (read?.target === path.join(source, OWNER)) ownerRead = true;
      if (read?.target === draft && !injected && read.text === INITIAL) {
        fs.writeFileSync(draft, INJECTED);
        injected = true;
        emit({ type: 'user_edit_inserted', sha256: hash(INJECTED) });
      } else if (read?.target === draft && injected && read.text === INJECTED) {
        reread = true;
      }
    }
    if (event.type === 'message_end' && event.message?.role === 'assistant') finalMessage = event.message.stopReason === 'stop';
    if (event.type === 'agent_settled') { settled = true; aborted = Boolean(event.aborted); }
  };
  const result = { id: 'T09', status: 'INCONCLUSIVE', verdict: 'UNREVIEWED', reason: null };
  let session;
  let unsubscribe;
  let timer;
  try {
    if (!sessionFactory) throw new Error('Live SDK requires explicit sandbox launcher/session factory');
    const deadline = new Promise((resolve, reject) => {
      timer = setTimeout(() => reject(new Error('Fixture deadline exceeded')), config.timeoutMs);
    });
    const work = (async () => {
      const created = await sessionFactory({ config, tools, system: `Read ${OWNER} first. Only supplied package Markdown and fixture/draft.md are available. Return text only; no spend or external actions.` });
      if (!active) { created.dispose(); return; }
      session = created;
      unsubscribe = session.subscribe(onEvent);
      await session.prompt(PROMPT);
      if (!active) return;
      if (!ownerRead || !injected || !reread || !settled || aborted || !finalMessage) throw new Error('Missing controlled read/re-read/final/settled evidence');
      result.status = 'completed';
      fs.writeFileSync(path.join(config.outputRoot, 'response.md'), session.getLastAssistantText(), { flag: 'wx' });
    })();
    await Promise.race([work, deadline]);
  } catch (error) {
    result.reason = error instanceof Error ? error.message : 'Unknown fixture adapter failure';
  } finally {
    active = false;
    clearTimeout(timer);
    unsubscribe?.();
    if (session) {
      // Dispose aborts active SDK work; closed tools reject late writes after timeout.
      session.dispose();
    }
  }
  const final = fs.readFileSync(draft, 'utf8');
  const summary = { ...result, injected, reread, initialSha256: hash(INITIAL), finalSha256: hash(final),
    matchesExpected: final === EXPECTED, prompt: PROMPT, promptSha256: hash(PROMPT) };
  fs.writeFileSync(path.join(config.outputRoot, 'execution-summary.json'), JSON.stringify(summary, null, 2), { flag: 'wx' });
  return summary;
}
