# Webhook: Receive Ping event

See [Receive GitHub webhook](post.md) for common behaviour.

**URL** : `/api/github/`

**Method** : `POST`

**Auth required** : NO

**Permissions required** : None

**Header constraints**

* `X-GitHub-Event: ping`

**Condition** : If everything is OK and an Account didn't exist for this User.

**Code** : `200 OK`

**Content example**

## Error Responses

**Condition** : If the set of events is not just `pull_request`.

**Code** : `400 BAD REQUEST`

**Content example** :

Given that the following hook events were sent:

```json
{
    "...": [],
    "hook": {
        "...": [],
        "events": [
            "push",
            "pull_request"
        ],
        "...": []
    },
    "...": []
}
```

Then the response will be:

```json
{
    "detail": {
        "events": [
            "This webhook only accepts \"pull_request\" events, plus the default \"ping\". Events received were \"['push', 'pull_request']\". Please reconfigure."
        ]
    }
}
```
