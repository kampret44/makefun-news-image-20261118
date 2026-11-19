// news-image-20261118 entrypoint (Node 22, standard library only).
//
// The entry image is rendered ahead of time by render.py and shipped in
// this repository as entry.png. At grade time the sandbox has no network,
// so this program simply places that file where the grader expects it:
// /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png when set, which is
// how the program is run locally).
//
// The copy is byte-for-byte, so two runs always produce identical output.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), target);
