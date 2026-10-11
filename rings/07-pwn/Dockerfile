FROM ubuntu:22.04 AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY antahkaranam.c Makefile ./
RUN make

FROM ubuntu:22.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    socat \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash ctf && \
    mkdir -p /sanctum /app && \
    chown -R root:ctf /sanctum /app && \
    chmod 750 /app

WORKDIR /app
COPY --from=builder /build/antahkaranam /app/antahkaranam
RUN chmod 755 /app/antahkaranam

# Sanctum artifacts (readable by the process / exploit payload)
RUN echo "BRIHADBALA_SANCTUM_COMPROMISED_7714" > /sanctum/token && \
    chmod 644 /sanctum/token
COPY sanctum/ /sanctum/
RUN chmod -R 644 /sanctum/*

USER ctf
EXPOSE 9007

CMD ["socat", "-T600", "TCP-LISTEN:9007,reuseaddr,fork", "EXEC:/app/antahkaranam,stderr"]
