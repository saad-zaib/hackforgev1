FROM php:8.0-apache

RUN apt-get update && apt-get install -y \
    iputils-ping \
    whois \
    dnsutils \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 80

CMD ["apache2-foreground"]
