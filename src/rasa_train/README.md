# RASA Command
| Command          | Effect |
|------------------|--------|
| `rasa init`      | Creates a new project with example training data, actions, and config files. |
| `rasa train`     | Trains a model using your NLU data and stories, saves trained model in ./models. |
| `rasa interactive` | Starts an interactive learning session to create new training data by chatting to your assistant. |
| `rasa shell`     | Loads your trained model and lets you talk to your assistant on the command line. |
| `rasa run`       | Starts a server with your trained model. |
| `rasa visualize` | Generates a visual representation of your stories. |
| `rasa test`      | Tests a trained Rasa model on any files starting with test_. |

# Training Process
1. `rasa init`  Creates a new project with config, data, domain, and training files.
2. modify `config.yml` to add pipeline and policies.
3. modify `data/nlu.yml` and `data/stories.yml` and `data/rules.yml`to add training data.
4. modify `domain.yml` to add actions, intents, entities, and slots.
5. `rasa train` Trains a model using your NLU data and stories, saves trained model in ./models.
6. `rasa interactive`  Starts an CDD training to create new training data by chatting.
7. `rasa shell`  Loads your trained model and lets you talk to your assistant on the command line.

# Specifications

    

# TODOS
- [ ] Add more training data(stories, nlu, rules) 
- [ ] Specify more actions intents and entities to the scripts
- [ ] Get more responses from the training process




