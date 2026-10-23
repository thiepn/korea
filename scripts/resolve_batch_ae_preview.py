"""Wait for exact-head Cloudflare success and export its actual branch-preview URL."""
import json,os,re,time,urllib.parse,urllib.request
sha=os.environ['KOREA_HEAD_SHA'];repo=os.environ['GITHUB_REPOSITORY']
endpoint=f'https://api.github.com/repos/{repo}/commits/{sha}/check-runs?per_page=100'
for attempt in range(120):
    request=urllib.request.Request(endpoint,headers={'Authorization':'Bearer '+os.environ['GITHUB_TOKEN'],'Accept':'application/vnd.github+json','User-Agent':'korea-batch-ae-ci'})
    with urllib.request.urlopen(request,timeout=30) as response:
        checks=json.load(response).get('check_runs',[])
    successful=[c for c in checks if c['name']=='Cloudflare Pages' and c['status']=='completed' and c['conclusion']=='success']
    if successful:
        summary=successful[-1].get('output',{}).get('summary','') or ''
        match=re.search(r"Branch Preview URL:.*?<a href=['\"](https://[^'\"]+\.pages\.dev)['\"]",summary,re.S|re.I)
        if not match:raise RuntimeError('Cloudflare success check has no branch-preview link')
        url=match.group(1).rstrip('/')
        host=urllib.parse.urlparse(url).hostname or ''
        if not (host.startswith('feat-batch-ae-') and host.endswith('.pages.dev')):raise RuntimeError('Unexpected Cloudflare host '+host)
        with open(os.environ['GITHUB_ENV'],'a',encoding='utf-8') as env:env.write('KOREA_PREVIEW_URL='+url+'\n')
        print('PASS exact-head Cloudflare branch preview '+url)
        break
    time.sleep(5)
else:
    raise RuntimeError('Cloudflare branch deployment did not pass within 10 minutes')
