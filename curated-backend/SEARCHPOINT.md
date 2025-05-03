### 🎥 YouTube Search Endpoint

**URL:** `/api/search/?q=your+keywords`

**Method:** `GET`

**Query Params:**

- `q` (required): The keyword to search YouTube for.

**Sample Response:**

```json

{
  "results": [
    {
      "videoId": "abc123",
      "title": "Learn Django in 10 Minutes",
      "description": "A quick tutorial...",
      "thumbnail": "https://i.ytimg.com/...",
      "channel": "CodeWithMe"
    },
    ...
  ]
}
```
