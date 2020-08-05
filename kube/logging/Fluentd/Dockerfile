FROM quay.io/fluentd_elasticsearch/fluentd:v3.0.2

#RUN buildDeps="sudo make gcc g++ libc-dev" \
RUN apt-get update \
   && apt-get install -y --no-install-recommends \
   build-essential \
   libmaxminddb-dev \
   libgeoip-dev 
RUN gem install geoip-c \
   && gem install fluent-plugin-geoip \
   && gem install fluent-plugin-route \
   && gem sources --clear-all \
   && apt-get purge -y --auto-remove \
                  -o APT::AutoRemove::RecommendsImportant=false \
                  $buildDeps \
   && rm -rf /var/lib/apt/lists/* \
   && rm -rf /tmp/* /var/tmp/* /usr/lib/ruby/gems/*/cache/*.gem
