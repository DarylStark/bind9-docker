# What is BIND 9

All network systems operate with network addresses, such as IPv4 and IPv6. The vast majority of humans find it easier to work with names rather than seemingly endless strings of network address digits. The earliest ARPANET systems (from which the Internet evolved) mapped names to addresses using a hosts file that was distributed to all entities whenever changes occurred. Operationally, such a system became rapidly unsustainable once there were more than 100 networked entities, which led to the specification and implementation of the Domain Name System that we use today.

BIND 9 is a complete implementation of the DNS protocol. BIND 9 can be configured (using its named.conf file) as an authoritative name server, a resolver, and, on supported hosts, a stub resolver. While large operators usually dedicate DNS servers to a single function per system, smaller operators will find that BIND 9’s flexible configuration features support multiple functions, such as a single DNS server acting as both an authoritative name server and a resolver.

(Source: [Bind 9 documentation](https://bind9.readthedocs.io/en/v9_18_4/chapter1.html#introduction))

# Why use BIND 9

BIND 9 has evolved to be a very flexible, full-featured DNS system. Whatever your application is, BIND 9 probably has the required features. As the first, oldest, and most commonly deployed solution, there are more network engineers who are already familiar with BIND 9 than with any other system.

BIND 9 is transparent open source, licensed under the MPL 2.0 license. Users are free to add functionality to BIND 9 and contribute back to the community through our open Gitlab.

(Source: [ISC website](https://www.isc.org/bind/))

# BIND Uses on the Internet

## Almost every Internet connection starts with a DNS lookup

Before your mail server sends an email, before your web browser displays a web page, there is a DNS lookup to resolve a DNS name to an IP address. Watch this DNS Fundamentals presentation from Eddy Winstead of ISC or read A Warm Welcome to DNS by Bert Hubert of PowerDNS.

## BIND 9 on the Internet

BIND is used successfully for every application from publishing the (DNSSEC-signed) DNS root zone and many top-level domains, to hosting providers who publish very large zone files with many small zones, to enterprises with both internal (private) and external zones, to service providers with large resolver farms.

(Source: [ISC website](https://www.isc.org/bind/))

# This Docker image

This Docker image is created by Daryl Stark in order to run a up-to-date version of BIND 9 without being dependant on the packages from major Linux distributions. The Docker image is based on Alpine and the BIND 9 application is compiled from source during the creating of this image. This results in a up-to-date version of BIND 9.

When starting a container using this Docker image without a `named.conf` file, a nearly empty configuration will be created and a key for the `rndc` application will be generated. The default configuration is enough to run BIND 9 as recursive DNS server but won't do any forwarding and will not be authoritive for any zones. If you need these functionality, you can configure BIND 9 to do, though.

## Quick start

To start a Docker container using this image, you can use the following command:

```bash
docker run \
    -it \
    -p 53:53 \
    -p 953:953 \
    -v config:/app/config \
    -v var:/app/var \
    -v log:/app/log \
    dast1986/darylstark-bind9:latest
```

The configuration will be placed in the `config` directory, the runtime files for BIND 9 will be placed in the `var` directory. The `logs` directory will not be used, but you can create a logging configuration for BIND 9 in `config/named.conf` if you want to enable logging.