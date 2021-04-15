# Django-base-user

mac : pip install psycopg2
```
env LDFLAGS='-L/usr/local/lib -L/usr/local/opt/openssl/lib
-L/usr/local/opt/readline/lib' pip install psycopg2==2.8.2
```

mac M1 : pip install 
```
brew install postgresql

brew link openssl

LDFLAGS="-L/opt/homebrew/opt/openssl@1.1/lib" CPPFLAGS="-I/opt/homebrew/opt/openssl@1.1/include" PKG_CONFIG_PATH="/opt/homebrew/opt/openssl@1.1/lib/pkgconfig" pip install psycopg2==2.8.6 psycopg2-binary==2.8.6
```

generate rsa key
```
openssl genrsa -out pri.pem 2048
openssl rsa -in pri.pem -out pub.pem -outform PEM -pubout
openssl rsa -in pri.pem -pubout -outform DER | openssl sha1 -c
```