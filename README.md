# Parent Radio HK

Making emergency radio channel for Hong Kong Parents

## Prerequisite

* Linux environment with Docker
* VLC for playback

## Build

```
docker build -t parent-radio-hk .
```

## Run

1. Create an `env.list` file with following content

    ```
    AZURE_KEY=<azure cognitive service key>
    AZURE_REGION=<azure cognitive service region>
    ```

2. Run the Docker container

    ```
    docker run --net=host --rm --env-file env.list -it parent-radio-hk
    ```

3. With another terminal, open the output stream, e.g.

    ```
    vlc udp://@127.0.0.1:12345
    ```

4. Post a message and hear it from VLC, e.g.

    ```
    curl -XPOST http://localhost:5000/messages -d '{"text":"testing"}'
    ```
