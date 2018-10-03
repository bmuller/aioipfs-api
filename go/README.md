# Autogenerate API Interface
First, make sure you have [go](https://golang.org/) installed.  Then:

```shell
git clone https://github.com/ipfs/http-api-docs "$GOPATH/src/github.com/ipfs/http-api-docs"
cd "$GOPATH/src/github.com/ipfs/http-api-docs"
make install
```

Then, back in this folder:

```shell
go run main.go > ../aioipfs_api/autoapi.py
```
