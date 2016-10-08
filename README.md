# OpenLiveQ
Unofficial tools for the NTCIR OpenLiveQ task.

## Classes
- An instance of `Query`, `q`, is a dictionary of strings where `q[query_id] = query` .
- An instance of `Run`, `r`, is a dictionary of lists where `r[query_id][index] = document_id` .

## Methods
- The `read(path)` methods read the file at `path`.
- The `write(path)` methods write the instance to the file at `path`.
