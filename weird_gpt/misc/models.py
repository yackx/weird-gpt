from openai import OpenAI

client = OpenAI()

def print_models():
    data = client.models.list()
    print(f'{"id":<40} {"created":<12} {"object":<12} {"owned_by":<12}')
    print('-' * 80)
    for model in data:
        print(f'{model.id:<40} {model.created:<12} {model.object:<12} {model.owned_by:<12}')


if __name__ == "__main__":
    print_models()
