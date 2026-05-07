import re, sys

src = open('/home/jack/ClaudeProjects/PokeMerge/style.css').read()

# Rename keyframes (defs + references) so they can't clash with wiki ones.
KEYFRAMES = ['auraFrames','legendFrames','bob','pop','auraPop',
             'coinPop','genPop','coinPulseSlow','coinPulseFast',
             'shardPulse','burst','offerArrive','fulfillPulse','wiltPop',
             'passClaimable']
for name in KEYFRAMES:
    # @keyframes <name>
    src = re.sub(rf'(@(?:-webkit-|-moz-)?keyframes\s+){name}\b', rf'\1pm-{name}', src)
    # animation: <name> ...   /  animation: <something> ... <name>
    # We'll do a wordy replacement: any standalone token == name preceded by either
    # 'animation:' or comma or space inside an animation declaration.
    src = re.sub(rf'(animation\s*:\s*)([^;]*?)\b{name}\b', rf'\1\2pm-{name}', src)

# Drop top-level html/body resets we don't want to leak.
src = re.sub(r'html,\s*body\s*\{[^}]*\}\s*', '', src)

# Extract the body { ... } declarations to apply on .pokemerge-app itself.
m = re.search(r'\bbody\s*\{([^}]*)\}', src)
body_decls = m.group(1).strip() if m else ''
src = re.sub(r'\bbody\s*\{[^}]*\}\s*', '', src, count=1)

# Split out @keyframes blocks (must live outside @scope per spec).
keyframes_chunks = []
def collect_kf(m):
    keyframes_chunks.append(m.group(0))
    return ''
# Match a full @keyframes block including its braces.
src = re.sub(r'@(?:-webkit-|-moz-)?keyframes\s+[^{]+\{(?:[^{}]*\{[^}]*\})*\s*\}', collect_kf, src)

out = []
out.append('/* Generated from /home/jack/ClaudeProjects/PokeMerge/style.css. */\n')
out.append('/* Edit the source and re-run tools/namespace_pm_css.py if you change anything. */\n\n')

# Page-level wrapper carries the body styles.
out.append('.pokemerge-app {\n  ' + body_decls + '\n}\n\n')

# Keyframes (renamed) live at the top level.
out.extend(c + '\n' for c in keyframes_chunks)
out.append('\n')

# Everything else goes inside @scope so selectors only bind to descendants.
out.append('@scope (.pokemerge-app) {\n')
out.append(src.strip() + '\n')
out.append('}\n')

open('/home/jack/ClaudeProjects/PokefindWiki/static/games/pokemerge/style.css', 'w').write(''.join(out))
print('wrote', sum(len(x) for x in out), 'chars')
