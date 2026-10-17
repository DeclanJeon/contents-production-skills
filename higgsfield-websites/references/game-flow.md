# Game flow — `--type game`

A game is a website whose template ships **realtime multiplayer rooms**. Same
CLI, same repo layout, same deploy and publish; what differs is what you write
and where the rules live.

Package gate applies throughout this flow (see `../SKILL.md`): the runtime check never auto-installs; every asset/cover generation is an authorized operation inside the approved scope; image jobs run through the authorized eligible image executor in-package, video/audio/3D stay eligible provider jobs.

Remote project creation, asset operations, pushes, live deployment, community
listing, and contest entry each need their own explicit authorization under the
shared gate. Building a game or opting into a listing does not authorize any
other operation. Run the commands below only after their individual permission
checks pass.

Games used to run on a separate engine with its own `higgsfield game` commands.
They don't any more — that engine is being retired, and its commands are gone.
Deploy a game to production with the website deploy workflow after explicit
deployment authorization. Community listing is a separate operation; do not
describe it as game deployment.

## Create

```bash
higgsfield website create --type game --category <genre> --subdomain <name>
```

- **`--category` is REQUIRED and must be a game genre** — `arcade`, `puzzle`,
  `shooter`, `platformer`, `rpg`, `strategy`, `racing`, `simulation`,
  `adventure`, `action`, `fighting`, `survival`, `horror`, `sports`,
  `card-board`, `education`, `endless-runner`, `moba`, `music-rhythm`,
  `sandbox-building`. Fetch the live list with `higgsfield website categories`;
  a site category (`cinematic`, `ads-marketing`, …) is rejected.
- **Do NOT pass `--template`.** A game scaffolds from the one template a game
  can use; naming any other is a 422.
- `--subdomain` as always — it becomes the live URL.

## Read the contract that ships with the repo

The scaffold's **`app/AGENTS.md`** is the authoritative contract, and it travels
with the code so it cannot drift from the template you actually got. Read it
before writing anything. In short:

| File | What it is | Edit? |
| --- | --- | --- |
| `app/src/logic.js` | **The game** — six pure functions | **Yes, this is the game** |
| `app/public/index.html` + `client.js` | The screen and the input | **Yes** |
| `app/src/room.ts` | Sockets, state, fan-out | Rarely |
| `app/src/worker.ts` | Routes `/ws/<room>` | Almost never |

The six exports are `meta`, `setup`, `validateAction`, `applyAction`,
`isGameOver`, `viewFor`. `bun run check:logic` enforces the mechanical rules as
part of the build — no imports, no `Date.now()`/`Math.random()`, JSON-serializable
state.

Two rules the checker cannot enforce and that decide whether the game is any
good:

- **`validateAction` is the only defence.** The client is untrusted and can send
  any action at any time. Whose turn it is, whether the move is in range,
  whether the target is legal — all of it belongs there.
- **`viewFor` is how you hide information.** What it returns is the *only* thing
  that player receives. For a card game return that player's hand and everyone
  else's card *count*, never the full state.

## Build, deploy, and publication

Run the game build checks as documented, then complete the cover and metadata
gate **before deployment**. A game is not complete or deployable while the
required real values are missing:

- `og_title`, `og_description`, `favicon_url`, `og_image_url`, and
  `marketplace_cover_url` in `app/src/app-meta.json`.
- The cover must use the user's independent game brand; never use the
  Higgsfield app lockup for a standalone game. Reuse approved art or follow
  `references/app-cover.md` through an eligible, separately authorized
  executor. Authorize any output upload/storage separately.

Deploy with `higgsfield website deploy <website_id>` only after explicit
deployment authorization. It ships the live game. Publishing with
`higgsfield website publish <website_id>` is a separate, optional community
listing of the deployed version and requires explicit listing authorization;
listing consent does not authorize assets, upload, push, or deployment.

## Testing it

The template ships vitest against the real workerd runtime
(`app/tests/room.test.ts`), driving the room through actual WebSockets. Run
`bun run test` in `app/`. A game whose rules you changed should get a test for
the rule — the suite is the safety net for the wire protocol every game shares.

Play-test with two browser tabs on a local runtime or safely reachable
authorized preview before deployment: rooms are per-path (`/ws/<room>`), so two
tabs on the same room join the same game. Do not deploy solely for testing.
After an independently authorized deployment, verify the deployed game
separately; that post-deploy check does not replace pre-deployment testing.

## Art and audio

The asset pipeline lives here too, under the `game-` prefix. Read
`references/game-design-system.md` FIRST — it settles the game profile, the core
loop and the asset manifest — then `references/game-stylization.md` to derive the
STYLE FORMULA every visual prompt reuses byte-for-byte. No visual should exist
before that formula does.

Then the reference matching each manifest row:

| Asset | Reference |
| --- | --- |
| Sprites, backgrounds, UI | `references/game-stylization.md` |
| Spritesheets / 2D animation | `references/game-2d-animation.md` |
| Tiles, walls, ground, PBR maps | `references/game-textures.md` |
| Any 3D model or animation | `references/game-3d-animation.md` |
| Non-humanoid procedural rigs | `references/game-procedural-animation.md` |
| Music, SFX, voice | `references/game-audio.md` |
| Raw Meshy fallback | `references/game-meshy-api.md` |
| Before any image-to-3D submit | `references/game-meshy-input-rules.md` |

The GLB, rigging and texture tooling those references drive ships in this
skill's `scripts/` (`pipeline.py`, `glb_patch.py`, `rig_transfer.py`, …). Never
recreate a bundled script from memory — find it on disk.

Assets land in `app/public/`; keep `design/assets.csv` beside them so the
manifest travels with the game.

## Single-player is fine

Nothing here forces multiplayer. `meta: { minPlayers: 1, maxPlayers: 1 }` gives a
single-player game that still gets rooms, persistence and the same deploy — many
of the games on the platform are exactly that.
