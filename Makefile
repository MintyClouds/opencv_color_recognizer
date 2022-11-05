compose := docker compose

build:
	sudo $(compose) up --build -d

web-build:
	sudo $(compose) up --build -d web

up:
	sudo $(compose) up -d

stop:
	sudo $(compose) stop

down:
	sudo $(compose) down

ps:
	sudo $(compose) ps

logs-stream:
	sudo $(compose) logs -f stream_processer

logs-web:
	sudo $(compose) logs -f web