FROM rsalmei/clearly:0 AS patch-image

RUN apt-get update && apt-get upgrade -y

# --------------------------------------------------------------------

FROM patch-image

LABEL maintainer="Nicholas Elia <me@nichelia.com>"

ENV USER="nobody"
WORKDIR "/tmp"

USER ${USER}
