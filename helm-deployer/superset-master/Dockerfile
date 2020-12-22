FROM amancevice/superset:0.36.0

USER root

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
	&& curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list \
	&& wget https://download.dremio.com/odbc-driver/1.4.2.1003/dremio-odbc-1.4.2.1003-1.x86_64.rpm \
	&& apt-get update -y \
	&& ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
			build-essential \
			less \
			vim \
			openssh-server \
			telnet \
			openssl \
			net-tools \
			git \
			locales \
			sudo \
			dumb-init \
			curl \
			bsdtar \
			default-libmysqlclient-dev \
			libpq-dev \
			msodbcsql17 \
			mssql-tools \
			unixodbc-dev \
			alien \
    && pip install pyodbc \
	&& pip install sqlalchemy_dremio \ 
	&& alien -i dremio-odbc-1.4.2.1003-1.x86_64.rpm 

USER superset
