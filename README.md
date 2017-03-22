# OpenLiveQ
Unofficial tools for the NTCIR OpenLiveQ task.

## Classes
- An instance of `ClickThrough` is a dictionary of dictionaries where `ct[query_id][document_id][key] = value`
  - where each key is in `['mode_rank', 'ctr', 'male', 'female', '10-', '10+', ...]`
  - `ClickThrough::to_pagebias` measures page bias.
  - `ClickThrough::to_rankbias` measures rank bias.
  - `ClickThrough::to_relevance` generates faceted relevance data.
- An instance of `Query`, `q`, is a dictionary of strings where `q[query_id] = query` .
  - `Query::tokenize` generates a dictionary of bag-of-words for [tmanabe/BM25F](https://github.com/tmanabe/BM25F) .
- An instance of `QuestionData` is a dictionary from query IDs to listed dictionaries of document fields.
  - `QuestionData::write_bag_jags` generates a jag of bag-of-words for [tmanabe/BM25F](https://github.com/tmanabe/BM25F) using the global `serialize_bag_jag` .
  - `QuestionData::format` formats some other fields for the same library.
- An instance of `Run`, `r`, is a dictionary of lists where `r[query_id][index] = document_id` .

## Common methods
- The `read(path)` methods read the file at `path`.
- The `write(path)` methods write the instance to the file at `path`.
