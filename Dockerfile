FROM python:3.10-slim

WORKDIR /app

COPY . /app

CMD ["python", "-c", "from environment import Task1Env, Task2Env, Task3Env; \
print('Running smoke test...'); \
envs=[Task1Env(), Task2Env(), Task3Env()]; \
scores=[]; \
for e in envs: \
    obs=e.reset(); \
    done=False; \
    total=0; \
    while not done: \
        obs, r, done, info=e.step(__import__('models').Action.HOLD); \
        total+=r; \
    scores.append(e.agent_grader(e.stats)); \
print('Task Scores:', scores)"]