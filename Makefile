
d: dev
dev:
	TURBO_CONCURRENCY=25 npm run dev
b: build
build:
	npm run build
v: view
view:
	open 'http://localhost:3000'
c: clean
clean:
	rm -rf out
s: serve
	cd .next && python3 -m http.server 3002

.PHONY: d dev b build v view c clean