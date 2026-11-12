// Linux capability checks and an explicit, argv-only bwrap launch contract.
import * as fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

export function sandboxCommand(config, childArgs) {
  const source = fs.realpathSync(config.snapshotRoot);
  const fixture = fs.realpathSync(config.fixtureRoot);
  const evidence = fs.realpathSync(path.dirname(config.outputRoot));
  return ['bwrap', '--unshare-user', '--unshare-pid', '--die-with-parent', '--new-session',
    '--ro-bind', '/', '/', '--ro-bind', os.homedir(), os.homedir(),
    '--ro-bind', source, source, '--bind', fixture, fixture, '--bind', evidence, evidence,
    '--proc', '/proc', '--dev', '/dev', '--', process.execPath, ...childArgs];
}

export function assertSandbox(config) {
  const mounts = fs.readFileSync('/proc/self/mountinfo', 'utf8').trim().split('\n').map(line => {
    const fields = line.split(' ');
    return { point: fields[4].replace(/\\([0-7]{3})/g, (_, octal) => String.fromCharCode(parseInt(octal, 8))), options: fields[5].split(',') };
  });
  const has = (point, mode) => mounts.some(m => m.point === point && m.options.includes(mode));
  for (const point of ['/', os.homedir(), fs.realpathSync(config.snapshotRoot)]) {
    if (!has(point, 'ro')) throw new Error(`Required read-only sandbox mount absent: ${point}`);
  }
  for (const point of [fs.realpathSync(config.fixtureRoot), fs.realpathSync(path.dirname(config.outputRoot))]) {
    if (!has(point, 'rw')) throw new Error(`Required writable sandbox mount absent: ${point}`);
  }
}

export function probeSandbox(config) {
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'writing-sandbox-probe-'));
  try {
    const sentinel = path.join(temporary, 'sentinel');
    const envelope = path.join(temporary, 'evidence');
    fs.mkdirSync(envelope);
    fs.writeFileSync(sentinel, 'PRESERVE');
    const child = "const fs=require('node:fs');try{fs.writeFileSync(process.argv[1],'MUTATED');process.exitCode=7;}catch(e){if(!['EROFS','EACCES','EPERM'].includes(e.code))throw e;}";
    const command = sandboxCommand({ ...config, outputRoot: path.join(envelope, 'new-run') }, ['-e', child, sentinel]);
    const result = spawnSync(command[0], command.slice(1), { encoding: 'utf8', timeout: 5000, maxBuffer: 65536 });
    const preserved = fs.readFileSync(sentinel, 'utf8') === 'PRESERVE';
    return { supported: result.status === 0 && preserved, sentinelPreserved: preserved,
      reason: result.status === 0 && preserved ? null : result.error?.message || result.stderr || `Probe exit ${result.status}` };
  } finally {
    fs.rmSync(temporary, { recursive: true, force: true });
  }
}
