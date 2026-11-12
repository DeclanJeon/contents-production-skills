// Live bridge: only callable after explicit approval inside the checked bwrap mounts.
import * as fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
import { assertSandbox } from './writing_eval_sandbox.mjs';
import { runFixtureCase } from './writing_eval_fixture.mjs';

export async function createFixtureSession({ config, tools, system }) {
  if (config.liveApproved !== true) throw new Error('Explicit live evaluation approval required');
  assertSandbox(config);
  const packageRoot = fs.realpathSync(config.piPackage);
  const packageJson = path.join(packageRoot, 'package.json');
  const metadata = JSON.parse(fs.readFileSync(packageJson, 'utf8'));
  if (metadata.name !== '@earendil-works/pi-coding-agent') throw new Error('Unsupported SDK package');
  const sdk = await import(pathToFileURL(path.join(packageRoot, 'dist/index.js')).href);
  const require = createRequire(packageJson);
  const { Type } = await import(pathToFileURL(require.resolve('typebox')).href);
  const modelRuntime = await sdk.ModelRuntime.create({ allowModelNetwork: false, refreshOnCreate: false });
  const model = modelRuntime.getModel(config.provider, config.model);
  if (!model) throw new Error('Exact requested provider/model unavailable; no fallback permitted');
  const file = { path: Type.String() };
  const schemas = {
    read: Type.Object({ ...file, offset: Type.Optional(Type.Integer({ minimum: 1 })), limit: Type.Optional(Type.Integer({ minimum: 1 })) }, { additionalProperties: false }),
    edit: Type.Object({ ...file, oldText: Type.String({ minLength: 1 }), newText: Type.String() }, { additionalProperties: false }),
    write: Type.Object({ ...file, content: Type.String() }, { additionalProperties: false }),
  };
  const resourceLoader = {
    getExtensions: () => ({ extensions: [], errors: [], runtime: sdk.createExtensionRuntime() }),
    getSkills: () => ({ skills: [], diagnostics: [] }),
    getPrompts: () => ({ prompts: [], diagnostics: [] }),
    getThemes: () => ({ themes: [], diagnostics: [] }),
    getAgentsFiles: () => ({ agentsFiles: [] }),
    getSystemPrompt: () => system, getSystemPromptSource: () => undefined,
    getAppendSystemPrompt: () => [], getAppendSystemPromptSources: () => [],
    extendResources: () => {}, reload: async () => {},
  };
  const { session } = await sdk.createAgentSession({
    cwd: config.snapshotRoot, modelRuntime, model, thinkingLevel: config.thinking,
    settingsManager: sdk.SettingsManager.inMemory({ retry: { enabled: false, maxRetries: 0 }, compaction: { enabled: false } }),
    sessionManager: sdk.SessionManager.inMemory(config.snapshotRoot), resourceLoader,
    tools: ['read', 'edit', 'write'],
    customTools: tools.map(tool => ({
      name: tool.name, label: tool.name, description: tool.description,
      parameters: schemas[tool.name], executionMode: 'sequential',
      execute: async (id, args) => tool.execute(id, args),
    })),
  });
  if (session.model?.provider !== config.provider || session.model?.id !== config.model
      || session.getActiveToolNames().sort().join(',') !== 'edit,read,write') {
    session.dispose();
    throw new Error('Unexpected model fallback or tool selection');
  }
  return session;
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  if (process.argv.length !== 3) throw new Error('Usage: sandboxed node writing_eval_sdk.mjs <config.json>');
  const config = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const result = await runFixtureCase(config, createFixtureSession);
  process.stdout.write(JSON.stringify({ status: result.status, verdict: result.verdict }) + '\n');
  process.exitCode = result.status === 'completed' ? 0 : 2;
}
