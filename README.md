# pubnub-python-metrics

Interact with PubNub Metrics API and get cost details using python via the public rest api, using docker or locally using the cli.

## Public REST API
---

Currently the testing version of the public rest api is hosted on AWS Elastic Beanstalk with __minimal capabilities__. Will move into a EC2 instance in the future.

```bash
curl -i http://flask-env.eba-nam2bedw.us-east-1.elasticbeanstalk.com/v1/metrics/get_all_metrics \
-X POST \
-H 'Content-Type: application/json' \
-d '{"email":"email","password":"password","start_date":"2020-01-01","end_date":"2020-01-02"}'
```

## Docker
---

Install in a docker component and run the flask application on port 80.

```bash
docker build -t pubnub-python-metrics .
docker run --name ppm -p 80:80 pubnub-python-metrics
```

## Local CLI
---

### Local Package Install

Use the build_install.sh script to install the package locally.

```bash
chmod +x ./scripts/build_install.sh
./scripts/build_install.sh
```

### Local REST Server

```bash
python -m flask --app application.py run --host=0.0.0.0 -p 80
```

## Config
---

## Environment Variables (DOTENV)

Set in file `.env` in the root of your project.

```env
PN_CONSOLE_EMAIL=your_pn_console_email@your_domain.com
PN_CONSOLE_PASSWORD=your_pn_console_password
```

## Usage
---

### CLI Flags
===

```bash
pubnub-python-metrics --help
```

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

### REST API
===

#### Get Metrics by Date Range

```bash
curl -i http://127.0.0.1:80/v1/metrics/get_all_metrics -X POST -H 'Content-Type: application/json' -d '{"email": "mail@email.com", "password": "password", "start_date": "2022-12-01", "end_date": "2022-12-30"}' 
```