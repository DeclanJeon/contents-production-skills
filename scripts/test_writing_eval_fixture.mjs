import test from 'node:test';
import assert from 'node:assert/strict';
import * as fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const INITIAL = 'B01: 처음 문장입니다.\nB02: 루마를 봅니다.\nB03: 끝 문장입니다.\n';
const FINAL = 'B01: 사용자 수정 문장입니다.\nB02: 옷의 전체 윤곽을 봅니다.\nB03: 끝 문장입니다.\n';

function setup(t) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'writing-fixture-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const config = { snapshotRoot: path.join(root, 'source'), fixtureRoot: path.join(root, 'fixture'),
    outputRoot: path.join(root, 'out'), piPackage: '/not-used-for-offline-double',
    provider: 'test', model: 'offline-fake', thinking: 'low', timeoutMs: 200 };
  fs.mkdirSync(path.join(config.snapshotRoot, 'video-production-assets/references'), { recursive: true });
  fs.writeFileSync(path.join(config.snapshotRoot, 'video-production-assets/references/03-screenplay.md'), 'owner');
  fs.mkdirSync(config.fixtureRoot);
  fs.writeFileSync(path.join(config.fixtureRoot, 'draft.md'), INITIAL);
  fs.writeFileSync(path.join(config.fixtureRoot, 'neighbour.md'), 'preserve neighbour');
  return config;
}

function factory(mode = 'normal') {
  return async ({ tools }) => {
    let listener = () => {};
    let disposed = false;
    const byName = Object.fromEntries(tools.map(tool => [tool.name, tool]));
    const end = (id, name) => listener({ type: 'tool_execution_end', toolCallId: id, toolName: name, isError: false });
    return {
      subscribe(callback) { listener = callback; return () => { listener = () => {}; }; },
      async prompt() {
        if (mode === 'timeout') return new Promise(() => {});
        await byName.read.execute('owner', { path: 'video-production-assets/references/03-screenplay.md' }); end('owner', 'read');
        await byName.read.execute('r1', { path: 'fixture/draft.md' });
        if (mode !== 'missing_event') end('r1', 'read');
        if (mode === 'abort') { listener({ type: 'agent_settled', aborted: true }); return; }
        if (mode !== 'missing_reread') { await byName.read.execute('r2', { path: 'fixture/draft.md' }); end('r2', 'read'); }
        await byName.edit.execute('w1', { path: 'fixture/draft.md', oldText: 'B02: 루마를 봅니다.', newText: 'B02: 옷의 전체 윤곽을 봅니다.' });
        end('w1', 'edit');
        listener({ type: 'message_end', message: { role: 'assistant', stopReason: 'stop', content: [{ type: 'text', text: '수정했습니다.' }] } });
        listener({ type: 'agent_settled', aborted: false });
      },
      async abort() {},
      dispose() { disposed = true; },
      getLastAssistantText() { assert.equal(disposed, false); return '수정했습니다.'; },
    };
  };
}

test('fixture rejects parent, absolute and symlink escapes before opening them', async t => {
  const api = await import('./writing_eval_fixture.mjs');
  const config = setup(t);
  fs.symlinkSync(config.snapshotRoot, path.join(config.fixtureRoot, 'escape'));
  for (const requested of ['../source/secret', '/etc/passwd', 'fixture/neighbour.md', 'fixture/escape/file']) {
    assert.throws(() => api.resolveFixturePath(config.fixtureRoot, requested), /fixture|draft|path/i);
  }
  fs.renameSync(path.join(config.fixtureRoot, 'draft.md'), path.join(config.fixtureRoot, 'saved.md'));
  fs.symlinkSync(path.join(config.fixtureRoot, 'saved.md'), path.join(config.fixtureRoot, 'draft.md'));
  assert.throws(() => api.resolveFixturePath(config.fixtureRoot, 'fixture/draft.md'), /symlink|path/i);
});

test('user edit is inserted after initial read and preserved by the final write', async t => {
  const api = await import('./writing_eval_fixture.mjs');
  const config = setup(t);
  const result = await api.runFixtureCase(config, factory());
  assert.equal(result.status, 'completed');
  assert.equal(result.verdict, 'UNREVIEWED');
  assert.equal(fs.readFileSync(path.join(config.fixtureRoot, 'draft.md'), 'utf8'), FINAL);
  assert.equal(fs.readFileSync(path.join(config.fixtureRoot, 'neighbour.md'), 'utf8'), 'preserve neighbour');
  assert.equal(result.matchesExpected, true);
  const events = fs.readFileSync(path.join(config.outputRoot, 'events.jsonl'), 'utf8').trim().split('\n').map(JSON.parse);
  const initialEnd = events.findIndex(e => e.type === 'tool_execution_end' && e.toolCallId === 'r1');
  const insertion = events.findIndex(e => e.type === 'user_edit_inserted');
  const write = events.findIndex(e => e.type === 'fixture_written');
  assert.ok(initialEnd < insertion && insertion < write);
});

for (const mode of ['missing_event', 'missing_reread', 'abort', 'timeout']) {
  test(`incomplete ${mode} run is inconclusive and never overwrites stale contents`, async t => {
    const api = await import('./writing_eval_fixture.mjs');
    const config = setup(t);
    const result = await api.runFixtureCase(config, factory(mode));
    assert.equal(result.status, 'INCONCLUSIVE');
    assert.equal(result.verdict, 'UNREVIEWED');
    assert.notEqual(fs.readFileSync(path.join(config.fixtureRoot, 'draft.md'), 'utf8'), FINAL);
    assert.ok(fs.existsSync(path.join(config.outputRoot, 'execution-summary.json')));
  });
}

test('deadline covers session creation and prevents a late session from prompting', async t => {
  const api = await import('./writing_eval_fixture.mjs');
  const config = { ...setup(t), timeoutMs: 15 };
  let prompted = false;
  let disposed = false;
  const slowFactory = async () => {
    await new Promise(resolve => setTimeout(resolve, 90));
    return { prompt: async () => { prompted = true; }, subscribe: () => () => {}, dispose: () => { disposed = true; } };
  };
  const result = await api.runFixtureCase(config, slowFactory);
  assert.equal(result.status, 'INCONCLUSIVE');
  assert.match(result.reason, /deadline/i);
  await new Promise(resolve => setTimeout(resolve, 100));
  assert.equal(prompted, false);
  assert.equal(disposed, true);
});

test('partial initial read cannot trigger user insertion and evidence cannot be overwritten', async t => {
  const api = await import('./writing_eval_fixture.mjs');
  const config = setup(t);
  const partialFactory = async ({ tools }) => ({
    subscribe() { return () => {}; },
    async prompt() { await tools[0].execute('partial', { path: 'fixture/draft.md', limit: 1 }); },
    async abort() {}, dispose() {}, getLastAssistantText() { return ''; },
  });
  const result = await api.runFixtureCase(config, partialFactory);
  assert.equal(result.status, 'INCONCLUSIVE');
  assert.equal(fs.readFileSync(path.join(config.fixtureRoot, 'draft.md'), 'utf8'), INITIAL);
  await assert.rejects(api.runFixtureCase(config, factory()), /exist/i);
});

test('sandbox probe proves an external sentinel stays read-only', async t => {
  const api = await import('./writing_eval_sandbox.mjs');
  const config = setup(t);
  const probe = api.probeSandbox(config);
  assert.equal(typeof probe.supported, 'boolean');
  if (probe.supported) assert.equal(probe.sentinelPreserved, true);
  else assert.ok(probe.reason);
});

test('live SDK bridge refuses missing approval and an unsandboxed host before importing SDK', async t => {
  const api = await import('./writing_eval_sdk.mjs');
  const config = setup(t);
  await assert.rejects(api.createFixtureSession({ config, tools: [], system: '' }), /approval/i);
  await assert.rejects(api.createFixtureSession({ config: { ...config, liveApproved: true }, tools: [], system: '' }), /sandbox/i);
});

test('no factory does not submit a model request outside the sandbox launcher', async t => {
  const api = await import('./writing_eval_fixture.mjs');
  const config = setup(t);
  const result = await api.runFixtureCase(config);
  assert.equal(result.status, 'INCONCLUSIVE');
  assert.match(result.reason, /sandbox|factory/i);
});
