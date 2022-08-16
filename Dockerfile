# Base image
FROM alpine:latest

# Environment variables
ENV version=9.18.5

# Update repository
RUN apk update

# Install dependencies for ISC Bind
RUN apk add build-base pkgconfig perl libuv-dev nghttp2-dev openssl-dev libcap-dev

# Intall tools for this Docker image
RUN apk add python3 py3-pip

# Create application directories
RUN mkdir -p /app/bind9 /app/config /app/var /app/log /app/entrypoint

# Download BIND9 source-code
# https://downloads.isc.org/isc/bind9/<version>/bind-<version>.tar.xz
WORKDIR /root
RUN wget https://downloads.isc.org/isc/bind9/$version/bind-$version.tar.xz

# Extract source-code
RUN tar xf bind-$version.tar.xz

# Compile source-code
WORKDIR /root/bind-$version/
RUN CFLAGS="-Ofast" ./configure --prefix=/app/bind9 --sysconfdir=/app/config --localstatedir=/app/var
RUN make
RUN make install

# TODO: Remove source code

# Download root hints
RUN wget https://www.internic.net/domain/named.root -O /app/config/root.hints

# Create temporary configuration
# TODO: copy configuration from local
RUN touch /app/config/named.conf

# Copy the entry-point tool
COPY entrypoint/* /app/entrypoint/

# Install the entry-point tool
RUN pip3 install -r /app/entrypoint/requirements.txt

# Set execution permissions so it can be started
RUN chmod +x /app/entrypoint/start.py

# Expose the DNS port
EXPOSE 53/tcp
EXPOSE 52/udp
EXPOSE 953/tcp
EXPOSE 953/udp

# Set the entry point and CMD
# TODO: entry script
ENTRYPOINT [ "/app/entrypoint/start.py" ]
CMD [ "-g" ]