#!/usr/bin/env python
# coding: utf-8


class Query(dict):
    linebreak = '\n'
    separator = '\t'

    def read(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                query_id, query = line.split(Query.separator, 1)
                query = query.rstrip()
                self[query_id] = query
        return self

    def write(self, path):
        with open(path, 'w', encoding='utf-8') as file:
            for k in sorted(list(self.keys())):
                file.write(Query.separator.join([k, self[k]]))
                file.write(Query.linebreak)
        return self


class Run(dict):
    linebreak = '\n'
    separator = '\t'

    def __missing__(self, query_id):
        self[query_id] = []
        return self[query_id]

    def read(self, path):
        with open(path, 'r') as file:
            for line in file:
                query_id, document_id = line.split(Run.separator, 1)
                document_id = document_id.rstrip()
                self[query_id].append(document_id)
        return self

    def write(self, path):
        with open(path, 'w') as file:
            for query_id in sorted(list(self.keys())):
                document_ids = self[query_id]
                for document_id in document_ids:
                    line = Run.separator.join([query_id, document_id])
                    file.write(line)
                    file.write(Run.linebreak)
        return self
