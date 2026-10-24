# GROUP PROJECT

## System B (Kevin)

BM25 + RAG3 dense retrieval + weighted hybrid fusion + cross-encoder reranking,
with a single-pass answer generator and benchmark runner.
See [setup, commands, experimental controls, and limitations](docs/SYSTEM_B.md).

```sh
python -m src.system_b --help
python -m unittest discover -s tests -v
```

The existing baseline notebook and Docker environment are retained below.

```
In this branch, a vanilla RAG pipeline is being built in `build_agent.ipynb`. The project is made reproducible by using docker containerisation to package applications / libraries. 

Currently, only using a single financial statement (nvidia's latest statement) to test against the RAG pipeline. Tables are included within the text, but would likely be separated into tabular format instead for easier query. 
```
