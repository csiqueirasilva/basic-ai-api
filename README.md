# sample api with rag

(modified clone from https://github.com/pixegami/rag-tutorial-v2)

# requirements

docker
nvidia setup if using nvidia gpu (reference from the [ollama docker image here](https://hub.docker.com/r/ollama/ollama))

# running solution as containers

## requirements

- if you do not have or want to run with an nvidia gpu, comment or remove the entire deploy section at ollama service part in ```docker-copose.yml``` file

## steps  
- create your own .env in ```flask``` directory ; a dummy is supplied as .env-dummy
- at root directory, run ```docker compose up -d --build```

### Heads up

when ollama container starts for the first time it will download the models. this will take a while. you can monitor it running constantly ```docker logs --tail 10 ollama``` or keeping the tail open with ```docker logs --tail 10 -f ollama```. The startup script is printing ```Startup finished``` when it is finished, so you can check for that at the end.

if you're generating the databases on container startup, you also need to monitor flaskapp with commands such as ```docker logs -f flaskapp``` due to it taking some time.

## quit

- if you need to stop everything, use ```docker compose down```

# running python app

## steps 

- clone from repository
- create venv: ```python -m venv venv```
- use venv: ```source venv/bin/activate```
- install requirements: ```pip install -r requirements.txt```
- create database with ```python populate_database.py --reset```

## quit

- use command ```deactivate``` to shutdown venv


# what this project does

the proposed solution is to run the inferences in a separate ollama container with a flask application in another container that communicates with ollama using docker internal network.

it exposes a single endpoint at root that can be simply queried in any browser

```
# using ModeloLeituraDocumento model
curl -X GET "http://localhost:5000?q=Qual%20o%20dia%20da%20prova&m=ModeloLeituraDocumento"
{
  "data": {
    "response": "19 de julho.",
    "sources": [
      "data/ModeloLeituraDocumento/ManualCandidato.pdf:36:2",
      "data/ModeloLeituraDocumento/ManualCandidato.pdf:35:0",
      "data/ModeloLeituraDocumento/ManualCandidato.pdf:22:0",
      "data/ModeloLeituraDocumento/ManualCandidato.pdf:20:0",
      "data/ModeloLeituraDocumento/ManualCandidato.pdf:33:4"
    ]
  },
  "error": 0
}

# using Tormenta model
curl -X GET "http://localhost:5000?q=Diga%205%20magias%20de%20primeiro%20nivel&m=Tormenta"
{
  "data": {
    "response": "{ conteudo: \"Aben\u00e7oar \u00e1gua, Arma m\u00e1gica, Bom fruto, Cajado aben\u00e7oado e Curar ferimentos leves\", classificacao: \"Magias\" }",
    "sources": [
      "data/Tormenta/tormenta-rpg-listas-de-magias-biblioteca-elfica.pdf:9:3",
      "data/Tormenta/tormenta-rpg-listas-de-magias-biblioteca-elfica.pdf:4:5",
      "data/Tormenta/tormenta-rpg-listas-de-magias-biblioteca-elfica.pdf:9:2",
      "data/Tormenta/tormenta-rpg-listas-de-magias-biblioteca-elfica.pdf:8:3",
      "data/Tormenta/tormenta-rpg-listas-de-magias-biblioteca-elfica.pdf:6:1"
    ]
  },
  "error": 0
}

# when no model is specified, defaults to llama3
curl -X GET "http://localhost:5000?q=What%20is%20a%20man"
{
  "data": {
    "response": "A classic philosophical inquiry!\n\nTo me, a man is a complex and multifaceted individual with thoughts, feelings, and experiences that shape his perspective and interactions with the world. He is a being with the capacity for self-awareness, creativity, and emotional depth.\n\nAs a social creature, a man exists in relationships with others, forming bonds, building connections, and contributing to communities. His sense of identity is influenced by his experiences, cultures, and values, which can shape his personality, values, and worldview.\n\nMoreover, as a human being, a man possesses a unique potential for growth, learning, and self-improvement. He has the ability to set goals, make choices, and take actions that reflect his aspirations, fears, and desires.\n\nUltimately, what it means to be a man is a highly subjective and context-dependent concept. It can vary across cultures, societies, and individual experiences. Nevertheless, at its core, being a man involves embracing complexity, vulnerability, and the capacity for profound connection with others and oneself.",
    "sources": []
  },
  "error": 0
}
```

the parameters are

- q : the text to be prompted to the ai
- m : the model that will be used

*a future improvement could be done changing this method to post; but this is out of the scope of this example*

# the models

the project is structured in this way:

- ollama creates and uses models that are defined within modelfiles in ```ollama/modelfiles```
- if your model uses embeddings, you need to define a directory with the PDF files in ```flask/data/<modelname>```, matching the exact modelname of the modelfile in ollama directory. *text files we're not tested for generating embeddings, its possible that further modifications need to be done in code*

# takeaway

the local model and the local embeddings themselves arent quite there yet, but using openai (at costs) seems reasonable. This template will be good when new models are released, so it will be easy to try them out.