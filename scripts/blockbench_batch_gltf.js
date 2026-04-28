/**
 * Blockbench plugin: Batch convert .bbmodel files in a folder to .glb (glTF binary).
 *
 * Adds a menu item under Tools → "Batch Convert .bbmodel → .glb" that:
 *   1. Asks for an input folder of .bbmodel files
 *   2. Asks for an output folder
 *   3. Loads each .bbmodel, exports as .glb, closes the project, and moves on
 *   4. Reports a summary when done
 *
 * INSTALLATION:
 *   1. Open Blockbench
 *   2. File → Plugins → Load Plugin from File
 *   3. Pick this file (blockbench_batch_gltf.js)
 *   4. The new menu item appears under Tools (or File) — click it
 *
 * Tested on Blockbench 4.x (works on 4.10+ which the .bbmodel files were saved with).
 *
 * If the batch hangs partway through, open the dev console (Help → Developer Tools)
 * to see per-file error messages — usually a single bad model file we can skip.
 */

(function () {
    const PLUGIN_ID = 'pokefind_batch_gltf';
    let action;

    Plugin.register(PLUGIN_ID, {
        title: 'Batch glTF Export',
        author: 'Pokefind Wiki',
        description: 'Batch-convert a folder of .bbmodel files to .glb (glTF binary).',
        icon: 'fa-cogs',
        version: '1.0.0',
        variant: 'desktop',

        onload() {
            action = new Action(PLUGIN_ID, {
                name: 'Batch Convert .bbmodel → .glb',
                description: 'Pick a folder of .bbmodel files and export each as .glb.',
                icon: 'fa-cogs',
                click: function () {
                    runBatch().catch(err => {
                        console.error('[batch-gltf] fatal:', err);
                        Blockbench.showQuickMessage('Batch failed: ' + (err && err.message ? err.message : err), 4000);
                    });
                },
            });
            // Install under Tools menu; fall back to File menu if Tools doesn't exist
            try { MenuBar.addAction(action, 'tools'); }
            catch (_) { try { MenuBar.addAction(action, 'file.export'); } catch (__) {} }
        },

        onunload() {
            if (action) action.delete();
        },
    });

    // ----------------------------------------------------------------

    function pickDirectory(title) {
        return new Promise((resolve) => {
            // Blockbench wraps the Electron remote dialog
            Blockbench.pickDirectory({
                title: title,
                startpath: undefined,
                resource_id: 'pokefind_batch_gltf_dir',
            }, (path) => resolve(path || null));
        });
    }

    function listBbmodelFiles(dir) {
        const fs = require('fs');
        const path = require('path');
        return fs.readdirSync(dir)
            .filter(f => f.toLowerCase().endsWith('.bbmodel'))
            .map(f => path.join(dir, f));
    }

    async function loadBbmodel(filePath) {
        const fs = require('fs');
        const path = require('path');
        const content = fs.readFileSync(filePath, 'utf-8');
        // Use the project codec (handles .bbmodel) — read as a synthetic file drop.
        // Codecs.project is the standard .bbmodel codec on Blockbench 4.x.
        const codec = Codecs.project;
        if (!codec) throw new Error('Codecs.project not available');
        const fileObj = {
            path: filePath,
            name: path.basename(filePath),
            content: content,
        };
        codec.load(content, fileObj);
        // Wait one tick for Blockbench to finish setting up Project
        await new Promise(r => setTimeout(r, 60));
    }

    async function exportGlb(outPath) {
        const fs = require('fs');
        // Codecs.gltf is the GLTF/GLB codec
        const codec = Codecs.gltf;
        if (!codec) throw new Error('Codecs.gltf not available — install/enable the glTF plugin in Blockbench first');
        // Two API shapes appear across Blockbench versions:
        //   (a) codec.compile() returns a Promise resolving to ArrayBuffer/Buffer
        //   (b) codec.compile(options, callback)
        const result = await new Promise((resolve, reject) => {
            try {
                const ret = codec.compile({}, (data) => resolve(data));
                if (ret && typeof ret.then === 'function') {
                    ret.then(resolve, reject);
                } else if (ret !== undefined && ret !== null) {
                    // synchronous return
                    resolve(ret);
                }
                // else: callback path will fire
            } catch (e) {
                reject(e);
            }
        });
        let buf;
        if (result instanceof ArrayBuffer) {
            buf = Buffer.from(result);
        } else if (Buffer.isBuffer(result)) {
            buf = result;
        } else if (typeof result === 'string') {
            buf = Buffer.from(result, 'binary');
        } else if (result && result.buffer) {
            buf = Buffer.from(result.buffer);
        } else {
            throw new Error('Unrecognized GLTF compile result type: ' + (typeof result));
        }
        fs.writeFileSync(outPath, buf);
    }

    function closeProject() {
        // Tear down the current Project so the next load starts clean
        if (typeof Project !== 'undefined' && Project) {
            try { Project.close(true); } catch (_) {}
        }
        // Some Blockbench versions need an explicit ModelProject removal
        try {
            if (typeof ModelProject !== 'undefined' && ModelProject.all) {
                ModelProject.all.slice().forEach(p => {
                    try { p.close(true); } catch (_) {}
                });
            }
        } catch (_) {}
    }

    async function runBatch() {
        const inputDir = await pickDirectory('Pick the folder of .bbmodel files');
        if (!inputDir) return;
        const outputDir = await pickDirectory('Pick the output folder for .glb files');
        if (!outputDir) return;

        const path = require('path');
        const files = listBbmodelFiles(inputDir);
        if (!files.length) {
            Blockbench.showQuickMessage('No .bbmodel files found in ' + inputDir, 4000);
            return;
        }

        Blockbench.showQuickMessage(`Converting ${files.length} models…`, 2500);
        let ok = 0, failed = 0;
        const failures = [];

        for (let i = 0; i < files.length; i++) {
            const f = files[i];
            const baseName = path.basename(f, '.bbmodel');
            const outPath = path.join(outputDir, baseName + '.glb');
            try {
                closeProject();
                await loadBbmodel(f);
                await exportGlb(outPath);
                ok += 1;
                console.log(`[batch-gltf] (${i + 1}/${files.length}) ${baseName} -> ${outPath}`);
            } catch (e) {
                failed += 1;
                failures.push({ file: baseName, err: String(e && e.message ? e.message : e) });
                console.error(`[batch-gltf] FAIL ${baseName}:`, e);
            }
        }
        closeProject();

        const msg = `Done. ${ok} ok, ${failed} failed (of ${files.length}).`;
        Blockbench.showQuickMessage(msg, 6000);
        console.log('[batch-gltf] ' + msg);
        if (failures.length) {
            console.log('[batch-gltf] failures:');
            failures.forEach(f => console.log('  ' + f.file + ': ' + f.err));
        }
    }
})();
