# Receive GitHub webhook

This endpoint receives POST requests from GitHub.

Two events are handled: `pull_request` and `ping`. The event type is indicated
in the `X-GitHub-Event` header. Since these two request types have largely
different endpoint conditions they have been split into two different
documents:

* `pull_request`: [Receive Pull Request event](post_pull_request.md)
* `ping`: [Receive Ping event](post_ping.md)

All other events will be rejected with `403 FORBIDDEN`.

## Common constraints

All request to this endpoint will be checked as follows:

* Data delivered will match [GitHub's payload
specification](https://developer.github.com/webhooks/#payloads).

* Assert that the incoming pull request is from a repository that is registered
    with the service.

* Constraints of the individual webhook will then be evaluated.

**URL** : `/api/github/`

**Method** : `POST`

**Auth required** : NO

**Permissions required** : None

**Header constraints**

* `X-GitHub-Event`: Must be included and must be one of `pull_request` or
    `ping`.

## Success Responses

See individual documents for responses:

* `pull_request`: [Receive Pull Request event](post_pull_request.md)
* `ping`: [Receive Ping event](post_ping.md)

## Common Error Responses

Error responses are analysed in the order shown below. For example, if an
request from an unregistered repository sends an `issue_comment` event, then
the `401 UNAUTHORIZED` code is returned for the missing repository, rather than
`403 FORBIDDEN` for the bad webhook event.


**Condition** : Repository provided in payload does not exist in system.

**Code** : `401 UNAUTHORIZED`

**Data example** :

```json
{
    "...": [],
    "repository": {
        "id": 987654321,
        "...": []
    },
    "...": []
```

**Content example** :

```json
{
    "repository": {
        "id": [
            "Repository with id \"987654321\" is not registered with prlint."
        ]
    }
}
```

### Or

**Condition** : If header `X-GitHub-Event` does not contain valid event.

**Code** : `403 FORBIDDEN`

**Data example** :

    X-GitHub-Event: issues

**Content example** :

```json
{
    "detail": "The 'issues' event is not accepted by this webhook. Please reconfigure."
}
```
