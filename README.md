# 신림왁싱 — 무드선과 독립된 카페형 후기 사이트

이 ZIP의 **내용물 전체**를 한 GitHub 저장소의 최상위에 올립니다. Cloudflare Pages에서 저장소를 연결하고 Framework preset `None`, Build command **비움**, Build output directory `.`, Production branch `main`을 선택하세요. 첫 화면은 첨부된 원고의 본문이며 동일한 글을 `/blog/sillim-waxing-first-visit/`에서도 볼 수 있습니다.

## 새 글 추가

`content/example-post.json`을 복사해 `content/posts/새-슬러그.json`을 만들고 파일명과 `slug`를 맞추세요. `body`는 문단별 배열, `date`는 YYYY-MM-DD 형식입니다. 게시용 사진은 `assets/images/`에 넣고 `image`, `image2`에 WebP 확장자를 뺀 파일명을 적습니다. `main`에 push하면 GitHub Actions가 첫 화면과 `/blog/새-슬러그/`를 재생성해 커밋합니다. Actions 쓰기 권한이 없다면 `python3 scripts/build.py`를 로컬에서 실행하고 생성된 HTML을 커밋하세요. 원본 텍스트는 `content/source/신림왁싱 원고.txt`에 보관했습니다.

## 사이트 이름과 사진

`site.json`의 `name`은 신림왁싱이며 HTML title, 메타 설명, Open Graph, WebSite 구조화 데이터와 파비콘을 포함했습니다. 검색 결과의 `workers.dev` 표시를 신림왁싱으로 바꿀지는 검색엔진이 결정합니다. 배포 주소가 확정되면 `site.json`의 `site_url`에 `https://...` 전체 주소를 넣고 push하세요. 그러면 파비콘·썸네일의 절대 URL과 canonical 주소가 재생성됩니다. 네이버는 파비콘 주소에 절대 경로를 권장합니다. 고유 도메인을 연결했다면 그 주소를 사용하세요. 썸네일·배너·프로필 이미지는 제작한 연출 이미지로 실제 매장이나 시술 장면을 보여 주지 않습니다. 본문은 사용자가 제공한 원고이며, 게시 전 상호·방문 경험 등 사실 관계를 확인하세요. 브라질리언·슈가링·임산부 왁싱은 이 글의 방문 후기 내용이 아니며 별도 상담 주제로만 표기했습니다.

## 메인 배너 문의 링크

배너 전체를 클릭하면 카카오 채널로 이동합니다. 문구는 `scripts/build.py`의 `cafe_header`, 주소는 `site.json`의 `marketing_url`에서 수정할 수 있습니다.

## 사이트맵 · RSS · llms.txt

현재 주소 `https://sillimwaxing.pages.dev`를 `site.json`의 `site_url`에 적용했습니다. 저장소 루트의 `sitemap.xml`, `rss.xml`, `llms.txt`, `robots.txt`는 `python3 scripts/build.py`를 실행하면 `content/posts/*.json` 글 목록에 맞춰 다시 생성됩니다. GitHub Actions도 글을 추가하거나 사이트 주소를 변경하면 이 파일들을 함께 커밋합니다. 메인과 상세 페이지에는 RSS 발견 태그가 들어 있습니다. 나중에 맞춤 도메인으로 바꾸면 `site_url`만 새 주소로 수정해 push하세요.
