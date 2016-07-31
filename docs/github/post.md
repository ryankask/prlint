# Receive GitHub webhook

This endpoint receives POST requests from GitHub. Two events are handled:
`pull_request` and `ping`. All other events will be rejected with `403
FORBIDDEN`.

Data delivered will match [GitHub's payload
specification](https://developer.github.com/webhooks/#payloads). Only the
appropriate fields will be highlighted in examples.

**URL** : `/api/github/`

**Method** : `POST`

**Auth required** : NO

**Permissions required** : None

**Header constraints**

* `X-GitHub-Event`: Must be included and must be one of `pull_request` or
    `ping`.

**Data constraints**


**Data example** 

## Success Response

### Ping event

**Condition** : If everything is OK and an Account didn't exist for this User.

**Code** : `200 OK`

**Content example**

### Pull Request event


## Error Responses

### Ping event

**Condition** : If the set of events is not just `pull_request`.

**Code** : `400 BAD REQUEST`

**Content example** :

Given that the following events were sent:

```json
{
    "events": [
        "push",
        "pull_request"
    ]
}
```

Then the response will be:

```json
{
    "events": [
        "This webhook endpoint only accepts `pull_request` events, plus the default `ping`. Events received were [`push`, `pull_request`]. Please reconfigure."
    ]
}
```
