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
            "id": "WRNV7NVLNuA",
            "title": "How To Code In Python | Python For Beginners | Python Coding Tutorial | Python Training | Edureka",
            "description": "Edureka Python Certification Training (Use Code \"YOUTUBE20\"): ...",
            "thumbnail": "https://i.ytimg.com/vi/WRNV7NVLNuA/hqdefault.jpg",
            "channelTitle": "edureka!",
            "publishedAt": "2020-11-26T14:00:12Z",
            "relevance_score": 5,
            "likes": 3660,
            "comment_count": 39,
            "duration": "PT17M39S"
        },
    ...
  ]
}  
],
  "query": "python tutorial",
  "total_results": 1
}
```
