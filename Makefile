
d: dev
dev:
	npm run dev
b: build
build:
	npm run build
v: view
view:
	open 'http://localhost:3001'
	cd out && python3 -m http.server 3001
c: clean
clean:
	rm -rf out

.PHONY: d dev b build v view c clean