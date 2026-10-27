"""Builds the Gibbi Games website from the game source.
Usage: python3 tools/build.py <path to game source html>
Writes gibbis/index.html (a full standalone page). The hub page, manifests,
service worker and icons live alongside it and are edited directly."""
import sys, re, pathlib, time
root = pathlib.Path(__file__).resolve().parent.parent
src = pathlib.Path(sys.argv[1]).read_text()
title = re.search(r'<title>(.*?)</title>', src).group(1)
body_start = src.index('<div id="app">')
pre = src[:body_start].replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
pre = re.sub(r'<title>.*?</title>\n', '', pre)
head = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="Hatch a Gibbi, raise it, play games together and dress it up. A Gibbi Games original.">
<meta name="theme-color" content="#1BBEEE">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Gibbis">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="../icons/icon-180.png">
<link rel="icon" type="image/png" href="../icons/icon-192.png">
<style>*,*::before,*::after{{box-sizing:border-box}}:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0;font:14px system-ui,sans-serif}}img{{max-width:100%}}</style>
'''
ver = f"v{int(time.time())}"
updater = """<script>
/* Auto-update: home-screen apps resume instead of reloading, so check for a newer build when the app comes back. */
(function(){const B='%s';
function keep(){try{window.__gibbiSave&&window.__gibbiSave()}catch(e){}}
async function chk(){try{const r=await fetch('../version.json?t='+Date.now(),{cache:'no-store'});const j=await r.json();
if(j.v&&j.v!==B&&sessionStorage.getItem('gibbiReloaded')!==j.v){sessionStorage.setItem('gibbiReloaded',j.v);keep();location.reload()}}catch(e){}}
document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible')chk();else keep()});
addEventListener('pagehide',keep);addEventListener('pageshow',e=>{if(e.persisted)chk()});setTimeout(chk,1200);
})();
</script>
""" % ver
out = head + pre + '</head>\n<body>\n' + src[body_start:] + '\n' + updater + '</body>\n</html>\n'
out = out.replace("window.claude?.hot?.ready ? window.claude.hot.ready(start) : start(window.claude?.hot?.data ?? {});", "start({});")
(root / 'gibbis' / 'index.html').write_text(out)
sw = (root / 'sw.js').read_text()
sw = re.sub(r"const VERSION='[^']*'", f"const VERSION='{ver}'", sw)
(root / 'version.json').write_text('{"v":"%s"}\n' % ver)
(root / 'sw.js').write_text(sw)
print('built gibbis/index.html', len(out), 'bytes')
