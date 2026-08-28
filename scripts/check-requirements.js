#!/usr/bin/env node
/**
 * PopiAI Workshop — Comprobación de requisitos del equipo
 *
 * Verifica lo descrito en "Requisitos de sala y setup":
 *   1. Acceso HTTPS a los dominios usados durante el workshop
 *   2. Software instalado: Git, Node.js 20 LTS (+ npm), Docker + Docker Compose
 *   3. Al menos una herramienta de IA disponible: Claude Code, GitHub Copilot CLI o Codex
 *
 * Uso (Windows, Linux o macOS — solo necesita Node.js):
 *   node scripts/check-requirements.js
 *
 * Sale con código 1 si falla algún requisito obligatorio.
 */

'use strict';

const { execFileSync } = require('node:child_process');
const https = require('node:https');
const os = require('node:os');

const IS_WIN = process.platform === 'win32';
const REQUIRED_NODE_MAJOR = 20;
const TIMEOUT_MS = 8000;

// ---------------------------------------------------------------------------
// Definición de requisitos
// ---------------------------------------------------------------------------

const DOMAINS = [
  { host: 'github.com', why: 'clonar el material del workshop' },
  { host: 'raw.githubusercontent.com', why: 'contenido de GitHub (*.githubusercontent.com)' },
  { host: 'api.anthropic.com', why: 'API de Claude' },
  { host: 'claude.ai', why: 'herramienta de IA' },
  { host: 'registry.npmjs.org', why: 'dependencias npm' },
  { host: 'nodejs.org', why: 'Node.js' },
  { host: 'hub.docker.com', why: 'imagen de la base de datos' },
  { host: 'registry-1.docker.io', why: 'registro Docker (*.docker.io)' },
  { host: 'api.x.ai', why: 'API usada en los ejercicios del día 2' },
  { host: 'cdn.rebrickable.com', why: 'imágenes usadas en los ejercicios del día 2' },
];

const SOFTWARE = [
  {
    name: 'Git',
    cmd: 'git',
    args: ['--version'],
    hint: 'https://git-scm.com/downloads',
  },
  {
    name: 'Node.js',
    cmd: 'node',
    args: ['--version'],
    hint: `https://nodejs.org (versión ${REQUIRED_NODE_MAJOR} LTS)`,
    validate: (out) => {
      const major = parseInt(out.replace(/^v/, '').split('.')[0], 10);
      return major >= REQUIRED_NODE_MAJOR
        ? null
        : `se requiere Node.js ${REQUIRED_NODE_MAJOR}+ (tienes ${out})`;
    },
  },
  {
    name: 'npm',
    cmd: 'npm',
    args: ['--version'],
    hint: 'viene incluido con Node.js',
  },
  {
    name: 'Docker',
    cmd: 'docker',
    args: ['--version'],
    hint: 'https://docs.docker.com/get-docker/',
  },
  {
    name: 'Docker Compose',
    cmd: 'docker',
    args: ['compose', 'version'],
    hint: 'incluido en Docker Desktop; en Linux instala el plugin docker-compose-plugin',
  },
];

const AI_TOOLS = [
  { name: 'Claude Code', cmd: 'claude', args: ['--version'] },
  { name: 'GitHub Copilot CLI', cmd: 'copilot', args: ['--version'] },
  { name: 'Codex CLI', cmd: 'codex', args: ['--version'] },
];

// ---------------------------------------------------------------------------
// Utilidades
// ---------------------------------------------------------------------------

const useColor = process.stdout.isTTY && !process.env.NO_COLOR;
const c = (code, s) => (useColor ? `\x1b[${code}m${s}\x1b[0m` : s);
const green = (s) => c('32', s);
const red = (s) => c('31', s);
const yellow = (s) => c('33', s);
const bold = (s) => c('1', s);

const OK = green('✔');
const KO = red('✘');
const WARN = yellow('!');

function section(title) {
  console.log('');
  console.log(bold(title));
  console.log('-'.repeat(title.length));
}

/** Ejecuta un comando y devuelve su primera línea de salida, o null si no existe/falla. */
function run(cmd, args) {
  try {
    const out = execFileSync(cmd, args, {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore'],
      timeout: TIMEOUT_MS,
      shell: IS_WIN, // en Windows resuelve .cmd/.exe/.ps1 del PATH
      windowsHide: true,
    });
    return out.trim().split(/\r?\n/)[0] || '';
  } catch {
    return null;
  }
}

/** Comprueba acceso HTTPS a un host. Cualquier respuesta HTTP cuenta como accesible. */
function checkHttps(host) {
  return new Promise((resolve) => {
    const req = https.request(
      { host, port: 443, path: '/', method: 'HEAD', timeout: TIMEOUT_MS },
      (res) => {
        res.resume();
        resolve({ ok: true, detail: `HTTP ${res.statusCode}` });
      },
    );
    req.on('timeout', () => {
      req.destroy();
      resolve({ ok: false, detail: `sin respuesta en ${TIMEOUT_MS / 1000}s` });
    });
    req.on('error', (err) => resolve({ ok: false, detail: err.code || err.message }));
    req.end();
  });
}

// ---------------------------------------------------------------------------
// Comprobaciones
// ---------------------------------------------------------------------------

const failures = [];
const warnings = [];

function checkSystem() {
  section('Equipo');
  const ramGb = os.totalmem() / 1024 ** 3;
  const ramLabel = `${ramGb.toFixed(1)} GB de RAM`;
  if (ramGb < 7.5) {
    console.log(`  ${KO} ${ramLabel} — se requieren 8 GB (mejor 16)`);
    failures.push('RAM insuficiente (mínimo 8 GB)');
  } else if (ramGb < 15.5) {
    console.log(`  ${WARN} ${ramLabel} — suficiente, aunque se recomiendan 16 GB`);
    warnings.push('Menos de 16 GB de RAM (recomendado)');
  } else {
    console.log(`  ${OK} ${ramLabel}`);
  }
  console.log(`  ${OK} ${os.type()} ${os.release()} (${os.arch()})`);
}

async function checkDomains() {
  section('Acceso a dominios (HTTPS)');
  const results = await Promise.all(DOMAINS.map((d) => checkHttps(d.host)));
  results.forEach((r, i) => {
    const { host, why } = DOMAINS[i];
    if (r.ok) {
      console.log(`  ${OK} ${host.padEnd(28)} ${why}`);
    } else {
      console.log(`  ${KO} ${host.padEnd(28)} ${why} — ${red(r.detail)}`);
      failures.push(`Sin acceso HTTPS a ${host} (${r.detail})`);
    }
  });
}

function checkSoftware() {
  section('Software instalado');
  for (const sw of SOFTWARE) {
    const out = run(sw.cmd, sw.args);
    if (out === null) {
      console.log(`  ${KO} ${sw.name.padEnd(16)} no encontrado — ${sw.hint}`);
      failures.push(`${sw.name} no está instalado (${sw.hint})`);
      continue;
    }
    const problem = sw.validate ? sw.validate(out) : null;
    if (problem) {
      console.log(`  ${KO} ${sw.name.padEnd(16)} ${out} — ${problem}`);
      failures.push(`${sw.name}: ${problem}`);
    } else {
      console.log(`  ${OK} ${sw.name.padEnd(16)} ${out}`);
    }
  }

  // Docker instalado pero ¿el daemon está en marcha?
  if (run('docker', ['--version']) !== null) {
    const info = run('docker', ['info', '--format', '{{.ServerVersion}}']);
    if (info === null || info === '') {
      console.log(`  ${WARN} ${'Docker daemon'.padEnd(16)} no responde — arranca Docker Desktop / el servicio docker`);
      warnings.push('Docker está instalado pero el daemon no está en marcha');
    } else {
      console.log(`  ${OK} ${'Docker daemon'.padEnd(16)} en marcha (server ${info})`);
    }
  }
}

function checkAiTools() {
  section('Herramienta de IA (basta con una)');
  let found = 0;
  for (const tool of AI_TOOLS) {
    const out = run(tool.cmd, tool.args);
    if (out === null) {
      console.log(`  ${yellow('·')} ${tool.name.padEnd(20)} no encontrado (comando "${tool.cmd}")`);
    } else {
      console.log(`  ${OK} ${tool.name.padEnd(20)} ${out}`);
      found += 1;
    }
  }
  if (found === 0) {
    console.log(`  ${KO} Ninguna herramienta de IA disponible`);
    failures.push(
      'No se encontró Claude Code, GitHub Copilot CLI ni Codex CLI. ' +
        'Instala una: `npm install -g @anthropic-ai/claude-code`, ' +
        '`npm install -g @github/copilot` o `npm install -g @openai/codex`',
    );
  }
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

(async () => {
  console.log(bold('PopiAI × Power Electronics — Comprobación de requisitos del workshop'));

  checkSystem();
  await checkDomains();
  checkSoftware();
  checkAiTools();

  section('Resumen');
  if (warnings.length) {
    for (const w of warnings) console.log(`  ${WARN} ${w}`);
  }
  if (failures.length === 0) {
    console.log(`  ${OK} ${green('Todos los requisitos se cumplen. ¡Listo para el workshop!')}`);
    process.exit(0);
  }
  console.log(`  ${KO} ${red(`${failures.length} requisito(s) NO se cumplen:`)}`);
  for (const f of failures) console.log(`     - ${f}`);
  process.exit(1);
})();
