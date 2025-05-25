# Dash with redux improved

A minimal app that compares:
- implementing a flux/redux architecture in Dash, with payloads ([before](before))
- implementing a flux/redux architecture in Dash, action classes ([after](after))


# How to start

Install the project:
```bash
git clone https://github.com/petitapetitio/dash-with-redux-improved
cd dash-with-redux-improved

python -m venv ~/dev/venvs/dash-with-redux-improved
source ~/dev/venvs/dash-with-redux-improved/bin/activate
```

Run one of the app:
```bash
python before/app.py
```
```bash
python after/app.py
```

The two applications does the same thing. 

What's interesting is how their implementation differs!