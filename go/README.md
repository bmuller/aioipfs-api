> git clone https://github.com/ipfs/http-api-docs "$GOPATH/src/github.com/ipfs/http-api-docs"
> cd "$GOPATH/src/github.com/ipfs/http-api-docs"
> make install

then in this dir:
> go run main.go > ../aioipfs_api/autoapi.py
