Song Restful
===
Retrieve information about KPOP artists and songs.

It requires a token assigned to your account to access information.

## Prerequisites

```bash
$ pip install djangorestframework
$ pip install --upgrade google-api-python-client
$ pip install django-cors-headers
$ pip install psycopg2-binary
```

## How to
```bash
1. Register Your ID:
    http POST :8000/account/account-list/ email={your_email}
        password={your_password} username={your_username}
2. Retrieve Your Token:
    http --form POST :8000/api-token-auth/ username={username} password={password}
3. How to Search a song
    # http :8000/songownership/?search={title} 'Authorization: Token your_token_value'
4. How to Search an Artist
    # http :8000/artist/?search={title} 'Authorization: Token your_token_value'
5. How to Search an Album
    # http :8000/album/?search={title} 'Authorization: Token your_token_value'
     

```
