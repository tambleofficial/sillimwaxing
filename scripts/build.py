#!/usr/bin/env python3
"""Generate an article-first blog or cafe directly in the repository root."""
from pathlib import Path
from datetime import date
from urllib.parse import quote
import html,json,re
ROOT=Path(__file__).resolve().parents[1]
SITE=json.loads((ROOT/'site.json').read_text(encoding='utf-8'))
def h(v):return html.escape(str(v),quote=True)
def url(p):return '/blog/'+p['slug']+'/'
def art(p,secondary=False):
 image=p.get('image2' if secondary else 'image','consultation')
 if not re.fullmatch(r'[a-z0-9-]+',image):raise ValueError('invalid image name')
 return f'<img class="post-photo" src="/assets/images/{h(image)}.webp" alt="{h(p["category"])} 글을 위한 연출 사진" loading="lazy" width="1200" height="800">'
def load():
 posts=[];seen=set()
 for f in sorted((ROOT/'content/posts').glob('*.json')):
  p=json.loads(f.read_text(encoding='utf8'))
  for field in ('slug','title','summary','category','date','body'):
   if not p.get(field):raise ValueError(f'{f}: missing {field}')
  if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',p['slug']) or f.stem!=p['slug'] or p['slug'] in seen:raise ValueError(f'{f}: invalid or duplicate slug')
  date.fromisoformat(p['date'])
  if not isinstance(p['body'],list) or not all(isinstance(x,str) and x.strip() for x in p['body']):raise ValueError(f'{f}: body must contain paragraphs')
  seen.add(p['slug']);posts.append(p)
 return sorted(posts,key=lambda x:(x['date'],x['slug']),reverse=True)
def categories(posts):
 result=[]
 for p in posts:
  if p['category'] not in result:result.append(p['category'])
 return result
def cat_link(cat):return '/?category='+quote(cat)+'#archive'
def search_box():return '<form class="site-search" action="/" method="get" role="search"><label class="sr-only" for="q">글 검색</label><input id="q" name="q" type="search" placeholder="이곳의 글 검색"><button aria-label="검색" type="submit">⌕</button></form>'
def nav(posts):
 return '<nav class="main-nav" aria-label="카테고리"><div class="nav-inner"><a href="/">홈</a><a href="/#archive">전체 글</a>'+''.join(f'<a href="{cat_link(c)}">{h(c)}</a>' for c in categories(posts))+'</div></nav>'
def head(p,kind,home=False):
 name=SITE['name'];color=SITE['colors']
 seo_title=SITE.get('seo_title',p['title']+' | '+name) if home else p['title']
 description=p.get('meta_description',p['summary'])
 base=SITE.get('site_url','').rstrip('/')
 image=base+'/assets/images/'+p.get('image','waxing-thumbnail')+'.webp'
 canonical=f'<link rel="canonical" href="{h(base+("/" if home else url(p)))}">' if base else ''
 schema={'@context':'https://schema.org','@type':'WebSite','name':name}
 if base:schema['url']=base+'/'
 schema_json=json.dumps(schema,ensure_ascii=False).replace('<',r'\u003c')
 return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{h(description)}"><meta name="theme-color" content="{color[0]}"><meta name="application-name" content="{h(name)}"><meta property="og:type" content="{'website' if home else 'article'}"><meta property="og:site_name" content="{h(name)}"><meta property="og:title" content="{h(seo_title)}"><meta property="og:description" content="{h(description)}"><meta property="og:image" content="{h(image)}"><meta name="twitter:card" content="summary_large_image">{canonical}<title>{h(seo_title)}</title><link rel="icon" type="image/x-icon" href="{h(base+'/favicon.ico')}"><link rel="icon" type="image/svg+xml" href="{h(base+'/favicon.svg')}"><link rel="apple-touch-icon" href="{h(base+'/apple-touch-icon.png')}"><link rel="stylesheet" href="/assets/style.css"><script type="application/ld+json">{schema_json}</script><script defer src="/assets/app.js"></script></head><body class="{kind}" style="--ink:{color[0]};--paper:{color[1]};--accent:{color[2]}"><a class="skip" href="#main">본문으로 건너뛰기</a>'''
def blog_header(posts):
 return f'''<div class="utility"><div><span>블로그</span><a href="/#archive">전체 글</a></div></div><header class="blog-header"><div class="brand"><a href="/" class="brand-kicker">{h(SITE.get('english','INDEPENDENT JOURNAL'))}</a><a href="/" class="brand-name">{h(SITE['name'])}</a><p>{h(SITE.get('tagline',SITE['description']))}</p></div>{search_box()}</header>{nav(posts)}'''
def cafe_header(posts):
 mark=SITE.get('mark','✳')
 return f'''<header class="cafe-banner"><img class="cafe-banner-photo" src="/assets/images/banner.webp" alt="" width="1300" height="600"><div class="cafe-banner-inner"><span class="cafe-kicker">{h(SITE.get('english','OPEN COMMUNITY'))}</span><a class="cafe-brand" href="/">{h(SITE['name'])}<span class="banner-mark" aria-hidden="true">{mark}</span></a><p>{h(SITE.get('tagline',SITE['description']))}</p><span class="banner-caption">첫 방문부터 읽어 보는 왁싱 이야기</span></div></header>{nav(posts)}'''
def profile(posts):
 return f'''<section class="profile-panel"><img class="profile-photo" src="/assets/images/banner.webp" alt="왁싱 공간 연출 사진" width="280" height="145"><img class="profile-avatar profile-avatar-img" src="/assets/images/profile.webp" alt="" width="70" height="70"><h2>{h(SITE['name'])}</h2><span class="profile-label">{h(SITE.get('english','EDITORIAL LOG'))}</span><p>{h(SITE['description'])}</p><a class="profile-link" href="/#archive">전체 글 살펴보기 →</a></section>'''
def category_panel(posts):
 return '<section class="widget"><h2>카테고리</h2><a class="widget-link" href="/#archive">전체 글 <span>'+str(len(posts))+'</span></a>'+''.join(f'<a class="widget-link" href="{cat_link(c)}">{h(c)} <span>{sum(p["category"]==c for p in posts)}</span></a>' for c in categories(posts))+'</section>'
def recent_panel(posts,current):
 return '<section class="widget"><h2>최근에 쓴 글</h2><ol class="recent-list">'+''.join(f'<li><a href="{url(p)}"><small>{h(p["category"])} · {h(p["date"][5:])}</small><span>{h(p["title"])}</span></a></li>' for p in posts if p['slug']!=current['slug'])+'</ol></section>'
def blog_sidebar(posts,p):return f'<aside class="blog-aside" aria-label="블로그 정보">{profile(posts)}{category_panel(posts)}{recent_panel(posts,p)}</aside>'
def cafe_sidebar(posts,p):
 return f'''<aside class="cafe-aside" aria-label="모임 및 게시판"><div class="cafe-tabs"><b>모임 정보</b><span>게시판 안내</span></div>{profile(posts)}<div class="join-note">서로의 이야기를 편하게 읽어 주세요.</div>{search_box()}{category_panel(posts)}{recent_panel(posts,p)}</aside>'''
def archive(posts,p):
 items=''.join(f'''<li class="archive-row" data-category="{h(x['category'])}" data-search="{h(x['title']+' '+x['summary']+' '+x['category'])}"><a class="archive-thumb" href="{url(x)}" aria-label="{h(x['title'])}"><img src="/assets/images/{h(x.get('image','waxing-thumbnail'))}.webp" alt="" loading="lazy" width="100" height="68"></a><span class="archive-category">{h(x['category'])}</span><a href="{url(x)}">{h(x['title'])}</a><time datetime="{h(x['date'])}">{h(x['date'])}</time></li>''' for x in posts)
 return f'''<section class="archive" id="archive"><div class="archive-heading"><div><span>ALL POSTS</span><h2>{'이 블로그의 글' if SITE['type']=='blog' else '모두의 게시판'}</h2></div><strong>{len(posts)}개의 이야기</strong></div><ul class="archive-list">{items}</ul><p class="archive-empty" hidden>해당하는 글이 없습니다.</p></section>'''
def comment_box(p):
 comments=p.get('comments',[])
 items=''.join(f'<div class="comment-item"><span class="comment-avatar">{h(c["name"][:1])}</span><div><strong>{h(c["name"])}</strong><small>에디터 메모</small><p>{h(c["text"])}</p></div></div>' for c in comments)
 return f'<section class="comments" id="comments"><div class="comments-title"><h2>댓글 <span>{len(comments)}</span></h2><span>댓글 작성은 닫혀 있습니다.</span></div><div class="comment-list">{items}</div></section>'
def neighbors(posts,p):
 i=posts.index(p);before=posts[i-1] if i else None;after=posts[i+1] if i+1<len(posts) else None
 def entry(x,label):return f'<a href="{url(x)}"><span>{label}</span>{h(x["title"])}</a>' if x else ''
 return f'<div class="post-neighbors">{entry(before,"이전 글")}{entry(after,"다음 글")}</div>'
def post_body(p):
 paragraphs=p['body'];body=[]
 for i,text in enumerate(paragraphs):
  if i==3:body.append('<h2>예약까지 세 주가 걸린 이유</h2>')
  if i==7:body.append('<h2>상담과 첫 왁싱</h2>')
  if i==9:body.append('<h2>돌아오는 길에 남은 것</h2>')
  body.append(f'<p>{h(text).replace(chr(10),"<br>")}</p>')
  if i in (1,7):
   body.append(f'<figure>{art(p,secondary=i==7)}<figcaption>연출 이미지</figcaption></figure>')
 takeaways=p.get('takeaways',[])
 if takeaways:
  body.append('<div class="editor-summary"><strong>함께 확인할 왁싱 주제</strong><ul>'+''.join(f'<li>{h(t)}</li>' for t in takeaways)+'</ul></div>')
 return ''.join(body)
def post(p,posts):
 kind=SITE['type'];author=p.get('author',SITE.get('editor','에디터'))
 toolbar='<div class="post-toolbar"><a href="/#archive">글 목록</a><span> / </span><span>'+h(p['category'])+'</span><button type="button" class="copy-link">URL 복사</button></div>'
 actions='<div class="post-actions"><button class="like-button" type="button" aria-pressed="false">♡ 공감 <span class="like-count">0</span></button><a href="#comments">댓글 보기 ↓</a><button class="copy-link" type="button">공유하기 ↗</button></div>'
 if kind=='blog':
  byline=f'<img class="author-avatar author-avatar-img" src="/assets/images/profile.webp" alt="" width="37" height="37"><div><strong>{h(author)}</strong><time datetime="{h(p["date"])}">{h(p["date"])} · {h(SITE["name"])}</time></div>'
  heading=f'<div class="post-heading"><span class="post-category">{h(p["category"])}</span><h1>{h(p["title"])}</h1><div class="byline">{byline}</div></div>'
 else:
  byline=f'<img class="author-avatar author-avatar-img" src="/assets/images/profile.webp" alt="" width="37" height="37"><div><strong>{h(author)}</strong><time datetime="{h(p["date"])}">{h(p["date"])} · {h(SITE["name"])}</time></div>'
  heading=f'<div class="post-heading"><a class="post-category" href="{cat_link(p["category"])}">{h(p["category"])} ›</a><h1>{h(p["title"])}</h1><div class="byline">{byline}<a class="byline-comments" href="#comments">댓글 보기 ↓</a></div></div>'
 return f'''<article class="post-card" data-post="{h(p['slug'])}">{toolbar}{heading}<div class="post-content">{post_body(p)}<div class="post-signoff">— {h(author)}의 기록</div></div>{actions}</article>{neighbors(posts,p)}{comment_box(p)}{archive(posts,p)}'''
def page(p,posts,home=False):
 kind=SITE['type'];header=blog_header(posts) if kind=='blog' else cafe_header(posts)
 sidebar=blog_sidebar(posts,p) if kind=='blog' else cafe_sidebar(posts,p)
 if kind=='blog':main=f'<main id="main" class="blog-layout"><div class="main-column">{post(p,posts)}</div>{sidebar}</main>'
 else:main=f'<main id="main" class="cafe-layout">{sidebar}<div class="main-column">{post(p,posts)}</div></main>'
 return head(p,kind,home)+header+main+f'<footer class="footer"><span>{h(SITE["name"])} · 첫 방문과 상담을 읽는 기록</span><a href="/">맨 위로 ↑</a></footer></body></html>'
def main():
 posts=load();(ROOT/'index.html').write_text(page(posts[0],posts,home=True),encoding='utf8')
 for p in posts:
  folder=ROOT/'blog'/p['slug'];folder.mkdir(parents=True,exist_ok=True)
  (folder/'index.html').write_text(page(p,posts),encoding='utf8')
 print(f'{SITE["name"]}: article-first root + {len(posts)} /blog/ pages')
if __name__=='__main__':main()
