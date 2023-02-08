# pubnub-python-metrics
PubNub Metrics API using python

## Requirements

This package depends on `probable-fiesta` which is a python base package builder with some extra features. You can find it here:

### MacOS

```bash
brew install python3
pip3 install probable-fiesta
pip3 install pubnub-python-metrics
```

## Config

## Environment Variables (DOTENV)

Set in file `.env` in the root of your project.

```env
PN_CONSOLE_EMAIL=your_pn_console_email@your_domain.com
PN_CONSOLE_PASSWORD=your_pn_console_password
```

## Build and Install

### Install locally

```bash
chmod +x ./scripts/build_install.sh
./scripts/build_install.sh
```

## Usage

```
pubnub-python-metrics --help
```

## Rest API

### Start flask server locally

```bash
flask --app app.server --debug run
```

### Get Metrics by Date Range

```bash
curl -i http://127.0.0.1:5000/v1/metrics/get_all_metrics -X POST -H 'Content-Type: application/json' -d '{"email": "mail@email.com", "password": "password", "start_date": "2022-12-01", "end_date": "2022-12-30"}' 
```

## Public API

```bash
curl -i http://flask-env.eba-nam2bedw.us-east-1.elasticbeanstalk.com/v1/metrics/get_all_metrics \
-X POST \
-H 'Content-Type: application/json' \
-d '{"email":"email","password":"password","start_date":"2020-01-01","end_date":"2020-01-02"}'
```

## Future Flags

### pubnub-python-metrics flags


#### --all_metrics

Return all metrics provided by the api. Unparsed. Raw.

#### --from

Returns all metrics from natural language date. Example: `--from "yesterday"`

__Note:__ Defaults to `today` if `--to` flag is not set.

#### --to

Returns all metrics to natural language date. Example: `--to "today"`

__Note:__ Requires `--from` flag.

### --cost

Returns all metrics for cost. Example: `--cost "replicated" --from "yesterday"` --to "today"` 


### probable-fiesta flags

#### --help

#### --version


## Modules

### Metrics

### PubNub Console User

__TODO:__ Move this to probable-fiesta
## probable-fiesta Modules

### Config

### Commands

### Parser

### Arguments
