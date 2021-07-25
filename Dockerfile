FROM rust:bullseye

ARG USER=user
ARG PORT=1337
ENV PORT ${PORT}

EXPOSE $PORT

RUN apt-get update -qy && apt-get install -qy socat

COPY challenge /challenge
RUN cargo install --path /challenge

RUN useradd -m ${USER}
WORKDIR /home/$USER/

ADD flag.txt flag.txt
CMD socat tcp-listen:${PORT},reuseaddr,fork exec:"hasher",su=user
