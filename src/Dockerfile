# Base image
FROM alpine:latest

# Set the workdir to download the software
WORKDIR /root

# Set the environment
ENV PATH="${PATH}:/app/bind9/bin:/app/bind9/sbin"

# Environment variables
ENV version=9.18.6

# Update repository
RUN apk update

# Install dependencies for ISC Bind
RUN apk add build-base pkgconfig perl libuv-dev nghttp2-dev openssl-dev libcap-dev

# Intall tools for this Docker image
RUN apk add python3 py3-pip

# Create application directories
RUN mkdir -p /app/bind9 /app/config /app/config-examples /app/var /app/log /app/entrypoint

# Download BIND9 source-code
RUN wget https://downloads.isc.org/isc/bind9/$version/bind-$version.tar.xz

# Extract source-code
RUN tar xf bind-$version.tar.xz

# Compile source-code
WORKDIR /root/bind-$version/
RUN CFLAGS="-Ofast" ./configure --prefix=/app/bind9 --sysconfdir=/app/config --localstatedir=/app/var
RUN make
RUN make install

# Remove source code
RUN rm -r /root/bind-$version/

# Download root hints
RUN wget https://www.internic.net/domain/named.root -O /app/config-examples/root.hints

# Copy configuration from local
COPY config-examples/ /app/config-examples/
RUN mv /app/config/bind.keys /app/config-examples/bind.keys

# Copy the entry-point tool
COPY entrypoint/* /app/entrypoint/

# Install the entry-point tool
RUN pip3 install -r /app/entrypoint/requirements.txt

# Set the directory for the container
WORKDIR /app

# Set execution permissions so it can be started
RUN chmod +x /app/entrypoint/start.py

# Expose the DNS port
EXPOSE 53/tcp
EXPOSE 52/udp
EXPOSE 953/tcp
EXPOSE 953/udp

# Set the entry point and CMD
ENTRYPOINT [ "/app/entrypoint/start.py" ]
