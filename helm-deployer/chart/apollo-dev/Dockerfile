FROM ubuntu:20.04
LABEL maintainer="Sean Connor <sean.connor@shell.com>"
ENV DEBIAN_FRONTEND=noninteractive

# install python, needed for yarn
RUN apt-get update -y && apt-get install -y \
	apt-transport-https \
	gnupg \
	wget \
	build-essential \
	curl \
	python3-pip python3-dev python3-setuptools \
	--no-install-recommends \
	&& rm -rf /var/lib/apt/lists/* \
  	&& cd /usr/local/bin \
  	&& ln -s /usr/bin/python3 python \
  	&& pip3 install --upgrade pip

# Install node
ENV NODE_VERSION="12.5.0"
RUN wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.35.1/install.sh | bash
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default ${NODE_VERSION}
RUN cp /root/.nvm/versions/node/v${NODE_VERSION}/bin/node /root/.nvm/versions/node/v${NODE_VERSION}/bin/npm /usr/bin/

# Install yarn
# https://yarnpkg.com/en/docs/install#debian-stable
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt-get update -y && apt-get install -y yarn

WORKDIR /app
COPY . ./
RUN mkdir /root/.aws
RUN yarn install
EXPOSE 4000
CMD [ "yarn", "start:production" ]