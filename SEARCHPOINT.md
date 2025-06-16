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
            "channelProfileImageUrl": "https://yt3.ggpht.com/a/AATXAJy.../s176-c-k-c0x00ffffff-no-rj-mo.jpg", // Example URL
            "publishedAt": "2020-11-26T14:00:12Z",
            "relevance_score": 5,
            "likes": 3660,
            "comment_count": 39,
            "view_count": 150000,
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
