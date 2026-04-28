/* ============================================================
   Blockbench dev-console batch converter — paste into console.
   ============================================================
   How to use:
   1. Open Blockbench
   2. Help → Developer Tools (or Ctrl+Shift+I)
   3. Click the Console tab
   4. Paste this whole snippet, hit Enter
   5. Watch the log lines for progress
   ============================================================ */

(async () => {
    const fs = require('fs');
    const path = require('path');

    const INPUT_DIR  = '/home/jack/Downloads/models';
    const OUTPUT_DIR = '/home/jack/ClaudeProjects/PokefindWiki/static/models/glb';

    if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });

    // ----------------------------------------------------------------
    // API probe — print available codecs so we can see what's actually here
    console.log('=== Codec probe ===');
    const codecKeys = Object.keys(Codecs || {});
    console.log('Codecs keys:', codecKeys);
    if (Codecs && Codecs.gltf) {
        console.log('gltf codec methods:', Object.keys(Codecs.gltf).filter(k => typeof Codecs.gltf[k] === 'function'));
    } else {
        console.error('Codecs.gltf NOT FOUND — enable the glTF format plugin in Blockbench (File → Plugins → search "glTF")');
        return;
    }
    if (!Codecs.project) {
        console.error('Codecs.project NOT FOUND');
        return;
    }

    // ----------------------------------------------------------------
    function closeAllProjects() {
        try {
            if (typeof ModelProject !== 'undefined' && ModelProject.all) {
                ModelProject.all.slice().forEach(p => {
                    try { p.close(true); } catch (_) {}
                });
            }
        } catch (_) {}
    }

    function loadBbmodel(filePath) {
        const content = fs.readFileSync(filePath, 'utf-8');
        // Pass to the project codec
        Codecs.project.load(content, { path: filePath, name: path.basename(filePath) });
    }

    async function exportGlb(outPath) {
        const codec = Codecs.gltf;
        // Try the various API shapes that exist across Blockbench versions
        let result;
        if (typeof codec.compile === 'function') {
            try {
                const ret = codec.compile({});
                if (ret && typeof ret.then === 'function') {
                    result = await ret;
                } else if (ret !== undefined) {
                    result = ret;
                }
            } catch (e) {
                // try callback form
                result = await new Promise((resolve, reject) => {
                    try { codec.compile({}, resolve); } catch (err) { reject(err); }
                });
            }
        }
        if (result === undefined && typeof codec.export === 'function') {
            // older API — calls save dialog. Skip; we want a path.
            throw new Error('Codecs.gltf.compile not available; only export() (interactive) exists in this Blockbench version');
        }
        if (result === undefined) {
            throw new Error('Codecs.gltf has no compile method');
        }
        let buf;
        if (result instanceof ArrayBuffer)        buf = Buffer.from(result);
        else if (Buffer.isBuffer(result))         buf = result;
        else if (typeof result === 'string')      buf = Buffer.from(result, 'binary');
        else if (result.buffer)                   buf = Buffer.from(result.buffer);
        else throw new Error('Unrecognized GLTF compile result type: ' + (typeof result));
        fs.writeFileSync(outPath, buf);
    }

    // ----------------------------------------------------------------
    const files = fs.readdirSync(INPUT_DIR).filter(f => f.toLowerCase().endsWith('.bbmodel'));
    console.log(`=== Found ${files.length} .bbmodel files ===`);

    let ok = 0, failed = 0;
    const fails = [];

    for (let i = 0; i < files.length; i++) {
        const f = files[i];
        const inPath = path.join(INPUT_DIR, f);
        const outPath = path.join(OUTPUT_DIR, f.replace(/\.bbmodel$/i, '.glb'));
        try {
            closeAllProjects();
            loadBbmodel(inPath);
            await new Promise(r => setTimeout(r, 80));   // let Blockbench finish setup
            await exportGlb(outPath);
            ok += 1;
            console.log(`(${i + 1}/${files.length}) OK  ${f}`);
        } catch (e) {
            failed += 1;
            fails.push({ f, err: String(e && e.message ? e.message : e) });
            console.error(`(${i + 1}/${files.length}) FAIL  ${f}:`, e);
        }
    }
    closeAllProjects();

    console.log(`=== Done: ${ok} ok, ${failed} failed (of ${files.length}) ===`);
    if (fails.length) console.log('Failures:', fails);
})();
