'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');
const assert = require('assert');
const test = require('node:test');

const {
  resolveMode,
  initRun,
  stepComplete,
  haltRun,
  runTests,
  readRunConfig,
  parseIssueIdFromCapture,
  validateStepGate,
  expectedNextStep,
  parseArtifactsArg,
  TEST_RESULTS_FILE,
} = require('./genesis-run.js');

const repoRoot = path.join(__dirname, '..');
const cliPath = path.join(__dirname, 'genesis-run.js');

function mkdtemp() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'pg-genesis-run-'));
}

function writeCapture(root, issueId = 'EPH-TEST-001') {
  fs.mkdirSync(path.join(root, '.ai', 'context'), { recursive: true });
  fs.writeFileSync(
    path.join(root, '.ai', 'context', 'last_capture.md'),
    `# Issue ID\n${issueId}\n`,
    'utf-8'
  );
}

test('resolveMode: CLI flags override env and default', () => {
  assert.strictEqual(resolveMode(['--autonomous'], {}), 'autonomous');
  assert.strictEqual(resolveMode(['--interactive'], { GENESIS_AUTONOMOUS: 'true' }), 'interactive');
  assert.strictEqual(resolveMode(['--interactive', '--autonomous'], {}), 'interactive');
  assert.strictEqual(resolveMode([], { GENESIS_AUTONOMOUS: 'yes' }), 'autonomous');
  assert.strictEqual(resolveMode([], { GENESIS_AUTONOMOUS: '1' }), 'autonomous');
  assert.strictEqual(resolveMode([], {}), 'interactive');
});

test('initRun writes run_config.json and reads issue id from capture', () => {
  const root = mkdtemp();
  try {
    writeCapture(root);

    const config = initRun(root, { mode: 'autonomous', reflect: true });
    assert.strictEqual(config.mode, 'autonomous');
    assert.strictEqual(config.issue_id, 'EPH-TEST-001');
    assert.strictEqual(config.reflect, true);
    assert.strictEqual(config.halted, false);

    const onDisk = readRunConfig(root);
    assert.ok(onDisk);
    assert.strictEqual(onDisk.mode, 'autonomous');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('initRun upgrades interactive to autonomous mid-run (preserves steps)', () => {
  const root = mkdtemp();
  try {
    writeCapture(root);
    initRun(root, { mode: 'interactive' });
    stepComplete(root, 'capture', ['.ai/context/last_capture.md'], { skipGateCheck: true });
    stepComplete(root, 'explore', ['.ai/context/last_explore.md'], { skipGateCheck: true });

    const upgraded = initRun(root, { mode: 'autonomous' });
    assert.strictEqual(upgraded.mode, 'autonomous');
    assert.ok(upgraded.mode_engaged_at);
    assert.strictEqual(upgraded.steps.length, 2);
    assert.strictEqual(expectedNextStep(upgraded), 'design_decisions');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('initRun rejects autonomous to interactive downgrade', () => {
  const root = mkdtemp();
  try {
    initRun(root, { mode: 'autonomous' });
    assert.throws(
      () => initRun(root, { mode: 'interactive' }),
      /cannot change/
    );
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('initRun re-init same mode updates reflect and issue_id', () => {
  const root = mkdtemp();
  try {
    writeCapture(root, 'EPH-OLD');
    initRun(root, { mode: 'interactive', reflect: false });

    writeCapture(root, 'EPH-NEW');
    const updated = initRun(root, { mode: 'interactive', reflect: true });

    assert.strictEqual(updated.issue_id, 'EPH-NEW');
    assert.strictEqual(updated.reflect, true);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('readRunConfig throws on corrupt JSON', () => {
  const root = mkdtemp();
  try {
    fs.mkdirSync(path.join(root, '.ai', 'context'), { recursive: true });
    fs.writeFileSync(path.join(root, '.ai', 'context', 'run_config.json'), '{bad', 'utf-8');
    assert.throws(() => readRunConfig(root), /Invalid run_config.json/);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('stepComplete appends steps without overwriting mode', () => {
  const root = mkdtemp();
  try {
    writeCapture(root);
    fs.writeFileSync(
      path.join(root, '.ai', 'context', 'last_capture.md'),
      '# Issue ID\nEPH-TEST-001\n',
      'utf-8'
    );
    initRun(root, { mode: 'autonomous' });
    stepComplete(root, 'capture', ['.ai/context/last_capture.md'], { skipGateCheck: true });
    const config = readRunConfig(root);
    assert.strictEqual(config.mode, 'autonomous');
    assert.strictEqual(config.steps.length, 1);
    assert.strictEqual(config.steps[0].name, 'capture');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('stepComplete throws when run is halted', () => {
  const root = mkdtemp();
  try {
    initRun(root, { mode: 'interactive' });
    haltRun(root, 'execute_plan', 'missing dependency');
    assert.throws(
      () => stepComplete(root, 'qa', [], { skipGateCheck: true }),
      /Run halted/
    );
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('stepComplete enforces artifact gates', () => {
  const root = mkdtemp();
  try {
    initRun(root, { mode: 'interactive' });
    assert.throws(
      () => stepComplete(root, 'capture'),
      /Step gate failed/
    );
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('stepComplete enforces step order', () => {
  const root = mkdtemp();
  try {
    writeCapture(root);
    initRun(root, { mode: 'interactive' });
    stepComplete(root, 'capture', ['.ai/context/last_capture.md'], { skipGateCheck: true });
    assert.throws(
      () => stepComplete(root, 'execute_plan', [], { skipGateCheck: true }),
      /Step order violation/
    );
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('validateStepGate detects missing capture issue id', () => {
  const root = mkdtemp();
  try {
    fs.mkdirSync(path.join(root, '.ai', 'context'), { recursive: true });
    fs.writeFileSync(
      path.join(root, '.ai', 'context', 'last_capture.md'),
      '# Title\nno issue id\n',
      'utf-8'
    );
    const gate = validateStepGate(root, 'capture');
    assert.strictEqual(gate.valid, false);
    assert.ok(gate.missing.some((m) => m.includes('Issue ID')));
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('expectedNextStep returns first step for empty config', () => {
  assert.strictEqual(expectedNextStep(null), 'capture');
  assert.strictEqual(expectedNextStep({ steps: [] }), 'capture');
});

test('parseArtifactsArg splits comma-separated paths', () => {
  const argv = ['step-complete', 'qa', '--artifacts', 'a.json,b.json', 'extra'];
  assert.deepStrictEqual(parseArtifactsArg(argv), ['a.json', 'b.json']);
});

test('haltRun sets halted fields', () => {
  const root = mkdtemp();
  try {
    initRun(root, { mode: 'interactive' });
    haltRun(root, 'execute_plan', 'missing dependency');
    const config = readRunConfig(root);
    assert.strictEqual(config.halted, true);
    assert.strictEqual(config.halt_step, 'execute_plan');
    assert.strictEqual(config.halt_reason, 'missing dependency');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('runTests writes test_results.json', () => {
  const root = mkdtemp();
  try {
    fs.writeFileSync(
      path.join(root, 'package.json'),
      JSON.stringify({
        name: 'test-pkg',
        scripts: { test: 'node -e "process.exit(0)"' },
      }),
      'utf-8'
    );

    const result = runTests(root, { attempt: 1 });
    assert.strictEqual(result.passed, true);

    const resultsPath = path.join(root, '.ai', 'context', TEST_RESULTS_FILE);
    assert.ok(fs.existsSync(resultsPath));
    const data = JSON.parse(fs.readFileSync(resultsPath, 'utf-8'));
    assert.strictEqual(data.final_passed, true);
    assert.strictEqual(data.attempts.length, 1);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('runTests rejects non-npm test commands', () => {
  const root = mkdtemp();
  try {
    assert.throws(() => runTests(root, { testCommand: 'rm -rf /' }), /Only "npm test"/);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('parseIssueIdFromCapture returns null when missing', () => {
  const root = mkdtemp();
  try {
    assert.strictEqual(parseIssueIdFromCapture(root), null);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('CLI init --autonomous upgrades interactive mid-run', () => {
  const root = mkdtemp();
  try {
    writeCapture(root);
    initRun(root, { mode: 'interactive' });
    stepComplete(root, 'capture', ['.ai/context/last_capture.md'], { skipGateCheck: true });

    const out = execSync(`node "${cliPath}" init --autonomous`, {
      cwd: root,
      encoding: 'utf-8',
    });
    const config = JSON.parse(out);
    assert.strictEqual(config.mode, 'autonomous');
    assert.strictEqual(config.steps.length, 1);
    assert.strictEqual(expectedNextStep(config), 'explore');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('CLI init --autonomous writes autonomous mode', () => {
  const root = mkdtemp();
  try {
    writeCapture(root);
    const out = execSync(`node "${cliPath}" init --autonomous`, {
      cwd: root,
      encoding: 'utf-8',
    });
    const config = JSON.parse(out);
    assert.strictEqual(config.mode, 'autonomous');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('CLI validate-gate fails without capture artifact', () => {
  const root = mkdtemp();
  try {
    initRun(root, { mode: 'interactive' });
    assert.throws(
      () => execSync(`node "${cliPath}" validate-gate capture`, { cwd: root, encoding: 'utf-8' }),
      /Command failed/
    );
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});
